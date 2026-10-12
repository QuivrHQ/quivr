package postgres

import (
	"context"
	"fmt"
	"testing"
	"time"
)

// Mixed-version freshness belongs here: old binaries omit the new write hooks.
// A bounded resumable pass must repair those omissions, retain availability
// after initialization, and remove cached work whose canonical row was deleted.
func TestQueueReconciliationRepairsPreviousWriterChanges(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	pool := queueWorkPool(t, ctx)
	if err := Migrate(ctx, pool); err != nil {
		t.Fatal(err)
	}
	seedQueueCorpus(t, ctx, pool, "example")
	for i := 1; i <= 3; i++ {
		seedQueueRecord(t, ctx, pool, "example", fmt.Sprintf("record-%d", i), fmt.Sprintf("version-%d", i), "text", "idle", 1, true)
	}
	snapshots := QueueSnapshots{Pool: pool}
	for {
		more, err := snapshots.Maintain(ctx)
		if err != nil {
			t.Fatal(err)
		}
		if !more {
			break
		}
	}
	exec := func(sql string) {
		t.Helper()
		if _, err := pool.Exec(ctx, sql); err != nil {
			t.Fatal(err)
		}
	}
	total := func(want int64) {
		t.Helper()
		var n int64
		if err := pool.QueryRow(ctx, `SELECT sum(pending)::bigint FROM queue_backlog_totals WHERE queue='live'`).Scan(&n); err != nil || n != want {
			t.Fatalf("maintained live=%d want=%d error=%v", n, want, err)
		}
	}
	// These mutations deliberately omit application observation, as the previous
	// binary does. Every Record key precedes the completed scan's restart point.
	exec(`UPDATE record_versions SET enrichment_state='queued'`)
	total(0)
	page := func(commit bool) (more bool) {
		t.Helper()
		tx, err := pool.Begin(ctx)
		if err != nil {
			t.Fatal(err)
		}
		defer tx.Rollback(ctx)
		more, err = advanceQueueBacklogBootstrap(ctx, tx, 2)
		if err != nil {
			t.Fatal(err)
		}
		if commit {
			if err := tx.Commit(ctx); err != nil {
				t.Fatal(err)
			}
		}
		return
	}
	if page(true) {
		t.Fatal("reconciliation ran before its next_run")
	}
	total(0)
	exec(`UPDATE queue_backlog_bootstrap SET next_run='-infinity'`)
	if !page(false) {
		t.Fatal("rollback page did not find pending work")
	}
	total(0)
	if !page(true) {
		t.Fatal("first page was not bounded")
	}
	total(2)
	var initialized bool
	var cursor string
	if err := pool.QueryRow(ctx, `SELECT initialized,record_id FROM queue_backlog_bootstrap WHERE singleton`).Scan(&initialized, &cursor); err != nil || !initialized || cursor != "record-2" {
		t.Fatalf("reconciliation progress=(%v,%s) error=%v", initialized, cursor, err)
	}
	if page(true) {
		t.Fatal("reconciliation did not finish")
	}
	total(3)
	// An old writer can also delete work after it was counted. The retained
	// observation key must still be visited, although the Record has disappeared.
	exec(`DELETE FROM accepted_revisions WHERE record_id='record-1'; DELETE FROM record_versions WHERE record_id='record-1'; DELETE FROM records WHERE id='record-1'; UPDATE queue_backlog_bootstrap SET next_run='-infinity'`)
	for page(true) {
	}
	total(2)
	exec(`INSERT INTO ingestion_receipts(organization,id,request_key,canonical_request,command,corpus_id,record_id,acceptance_order,slot,digest)
 VALUES('example','old-receipt','old-receipt','','{}','corpus','record-2',1,'text','old'); UPDATE queue_metric_bootstrap SET next_run='-infinity' WHERE source='ingestion'`)
	metricPage := func() bool {
		t.Helper()
		tx, err := pool.Begin(ctx)
		if err != nil {
			t.Fatal(err)
		}
		defer tx.Rollback(ctx)
		more, err := advanceQueueMetricBootstrap(ctx, tx, 2)
		if err != nil {
			t.Fatal(err)
		}
		if err := tx.Commit(ctx); err != nil {
			t.Fatal(err)
		}
		return more
	}
	for metricPage() {
	}
	pending, _, err := (MaterializationStore{Pool: pool}).IngestionBacklog(ctx)
	if err != nil || pending != 1 {
		t.Fatalf("old writer receipt reconciliation pending=%d error=%v", pending, err)
	}
	exec(`DELETE FROM ingestion_receipts WHERE id='old-receipt'; UPDATE queue_metric_bootstrap SET next_run='-infinity' WHERE source='ingestion'`)
	for metricPage() {
	}
	pending, _, err = (MaterializationStore{Pool: pool}).IngestionBacklog(ctx)
	if err != nil || pending != 0 {
		t.Fatalf("deleted old receipt still counted pending=%d error=%v", pending, err)
	}
}

// A scope transition must commit without reading every item. The scope's
// source table is deliberately unavailable; paged repair happens afterward.
func TestQueueOperationTransitionDoesNotReadWholeScope(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	pool := queueWorkPool(t, ctx)
	if err := Migrate(ctx, pool); err != nil {
		t.Fatal(err)
	}
	seedQueueCorpus(t, ctx, pool, "example")
	if _, err := pool.Exec(ctx, `INSERT INTO projection_generations(id,collection,profile_version) VALUES('target','target','example'); INSERT INTO operations(organization,id,kind,corpus_id,request_key,canonical_request,target_generation_id) VALUES('example','scope','quarantine_reprocess','corpus','scope','','target')`); err != nil {
		t.Fatal(err)
	}
	locked, err := pool.Begin(ctx)
	if err != nil {
		t.Fatal(err)
	}
	defer locked.Rollback(ctx)
	if _, err = locked.Exec(ctx, `LOCK quarantine_reprocess_items IN ACCESS EXCLUSIVE MODE`); err != nil {
		t.Fatal(err)
	}
	tx, err := pool.Begin(ctx)
	if err != nil {
		t.Fatal(err)
	}
	defer tx.Rollback(ctx)
	if _, err = tx.Exec(ctx, `SET LOCAL lock_timeout='100ms'`); err != nil {
		t.Fatal(err)
	}
	if err = lockJournal(ctx, tx, "example"); err != nil {
		t.Fatal(err)
	}
	if err = operationEvent(ctx, tx, "example", "corpus", "scope", "queued"); err != nil {
		t.Fatalf("scope transition read unavailable items: %v", err)
	}
	if err = tx.Commit(ctx); err != nil {
		t.Fatal(err)
	}
	if err = locked.Rollback(ctx); err != nil {
		t.Fatal(err)
	}
	for i := 1; i <= 3; i++ {
		seedQueueRecord(t, ctx, pool, "example", fmt.Sprintf("record-%d", i), fmt.Sprintf("version-%d", i), "text", "idle", 1, true)
		if _, err = pool.Exec(ctx, `INSERT INTO quarantine_reprocess_items(organization,operation_id,version_id,record_id,receipt_id,stage,previous) VALUES('example','scope',$1,$2,'','ingestion','{}')`, fmt.Sprintf("version-%d", i), fmt.Sprintf("record-%d", i)); err != nil {
			t.Fatal(err)
		}
	}
	// Initialize ordinary observations without consuming the targeted request.
	bootstrap, err := pool.Begin(ctx)
	if err != nil {
		t.Fatal(err)
	}
	defer bootstrap.Rollback(ctx)
	if _, err = bootstrap.Exec(ctx, `INSERT INTO queue_backlog_bootstrap(singleton,initialized,next_run) VALUES(true,true,'infinity'); INSERT INTO queue_backlog_totals(stripe,queue) SELECT s,q FROM generate_series(0,63) s CROSS JOIN (VALUES('live'),('bulk')) queues(q)`); err != nil {
		t.Fatal(err)
	}
	if err = bootstrap.Commit(ctx); err != nil {
		t.Fatal(err)
	}
	snapshots := QueueSnapshots{Pool: pool, RefreshInterval: time.Nanosecond}
	page := func(commit bool) {
		t.Helper()
		step, err := pool.Begin(ctx)
		if err != nil {
			t.Fatal(err)
		}
		defer step.Rollback(ctx)
		if more, err := advanceQueueScopeReconciliation(ctx, step, 2); err != nil || !more {
			t.Fatalf("scope page=%v error=%v", more, err)
		}
		if commit {
			if err := step.Commit(ctx); err != nil {
				t.Fatal(err)
			}
		}
	}
	total := func(want int64) {
		t.Helper()
		var n int64
		if err := pool.QueryRow(ctx, `SELECT sum(pending)::bigint FROM queue_backlog_totals WHERE queue='bulk'`).Scan(&n); err != nil || n != want {
			t.Fatalf("scope total=%d want=%d error=%v", n, want, err)
		}
	}
	page(false)
	total(0)
	page(true)
	total(2)
	if err = snapshots.Refresh(ctx); err != nil {
		t.Fatal(err)
	}
	if _, err = snapshots.QueueBacklog(ctx); err == nil {
		t.Fatal("published partially repaired scope")
	}
	page(true)
	total(3)
	if err = snapshots.Refresh(ctx); err != nil {
		t.Fatal(err)
	}
	statuses, err := snapshots.QueueBacklog(ctx)
	if err != nil {
		t.Fatal(err)
	}
	for _, status := range statuses {
		if status.Queue == "bulk" && status.Waiting != 3 {
			t.Fatalf("completed scope=%+v", status)
		}
	}
}
