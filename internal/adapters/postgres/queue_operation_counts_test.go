package postgres

import (
	"context"
	"fmt"
	"testing"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/workqueue"
)

// Operation waiting is a progress signal from persisted scope/progress counters.
// Unlike the stage-count owner, this contract permits approximate overlap and
// remains available without enumerating the original documents again.
func TestQueueOperationBacklogUsesScopeAndProgressCounters(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	pool := queueWorkPool(t, ctx)
	if err := Migrate(ctx, pool); err != nil {
		t.Fatal(err)
	}
	seedQueueCorpus(t, ctx, pool, "example")
	exec := func(query string) {
		t.Helper()
		if _, err := pool.Exec(ctx, query); err != nil {
			t.Fatal(err)
		}
	}
	exec(`INSERT INTO projection_generations(id,collection,profile_version) VALUES('target','target','example');
INSERT INTO plugin_registrations(id,plugin_id,version,endpoint,manifest_digest,contributions,roles,state)
VALUES('registration','example.counter','1','http://example.invalid','example','{}','{}','active');
INSERT INTO operations(organization,id,kind,corpus_id,request_key,canonical_request,target_generation_id,counters,created_at)
VALUES('example','rebuild','projection_rebuild','corpus','rebuild','','target','{"versions_in_scope":8,"versions_covered":3,"versions_quarantined":1}',clock_timestamp()-interval '30 seconds'),
('example','backfill','backfill','corpus','backfill','','target','{"versions_in_scope":8,"versions_done":3,"versions_skipped":1}',clock_timestamp()-interval '30 seconds'),
('example','estimated','backfill','corpus','estimated','','target','{"versions_done":3,"versions_skipped":1}',clock_timestamp()-interval '30 seconds');
INSERT INTO backfills(organization,operation_id,registration_id,spaces,estimate)
VALUES('example','backfill','registration','{}','{"versions":100}'),('example','estimated','registration','{}','{"versions":9}')`)
	snapshots := QueueSnapshots{Pool: pool}
	if _, err := snapshots.Maintain(ctx); err != nil {
		t.Fatal(err)
	}
	read := func(waiting, active int64) {
		t.Helper()
		exec(`UPDATE queue_backlog_snapshots SET published_at='-infinity'`)
		if err := snapshots.Refresh(ctx); err != nil {
			t.Fatal(err)
		}
		statuses, err := snapshots.QueueBacklog(ctx)
		if err != nil {
			t.Fatal(err)
		}
		seen := map[string]bool{}
		for _, status := range statuses {
			queue := string(status.Queue)
			if (status.Queue != workqueue.Live && status.Queue != workqueue.Bulk) || seen[queue] {
				t.Fatalf("queue identities: %+v, want each live and bulk once", statuses)
			}
			seen[queue] = true
			if status.Queue == workqueue.Bulk && (status.Waiting != waiting || status.InProgress != active) {
				t.Fatalf("bulk=%+v, want waiting=%d active=%d", status, waiting, active)
			}
			if status.IngestionWaiting == nil || *status.IngestionWaiting != 0 {
				t.Fatalf("operation scope must not block acquisition: %+v", status)
			}
			if status.Queue == workqueue.Bulk && waiting > 0 && status.OldestAgeSeconds < 25 {
				t.Fatalf("operation admission age lost: %+v", status)
			}
		}
		if !seen[string(workqueue.Live)] || !seen[string(workqueue.Bulk)] {
			t.Fatalf("queue identities: %+v, want live and bulk", statuses)
		}
	}
	read(13, 0)
	// Two stage observations of the same executing document consume one unit
	// of the operation's remaining scope and one in-progress document.
	exec(`INSERT INTO queue_document_attempts(organization,kind,work_id,document_id,token,lease_until)
VALUES('example','operation','rebuild','document',nextval('queue_document_attempt_tokens'),clock_timestamp()+interval '1 minute'),
('example','rebuild','rebuild','document',nextval('queue_document_attempt_tokens'),clock_timestamp()+interval '1 minute')`)
	read(12, 1)
	exec(`UPDATE operations SET state='paused' WHERE id='rebuild'`)
	read(9, 0)
	exec(`UPDATE operations SET counters=counters || '{"versions_done":30}' WHERE id IN ('backfill','estimated')`)
	read(0, 0)
	// Discovery must bound raw records before eligibility, persist progress only
	// on commit, and resume sparse corpora without skipping rejected records.
	for i := 1; i <= 7; i++ {
		seedQueueRecord(t, ctx, pool, "example", fmt.Sprintf("record-%d", i), fmt.Sprintf("version-%d", i), "text", "idle", 1, true)
	}
	exec(`UPDATE records SET withdrawn=true WHERE id<>'record-7'`)
	exec(`INSERT INTO operations(organization,id,kind,corpus_id,request_key,canonical_request,target_generation_id) VALUES('example','paged','projection_rebuild','corpus','paged','','target')`)
	page := func(commit bool) {
		t.Helper()
		tx, err := pool.Begin(ctx)
		if err != nil {
			t.Fatal(err)
		}
		defer tx.Rollback(ctx)
		if more, err := advanceQueueOperationScopes(ctx, tx, 2); err != nil || !more {
			t.Fatalf("scope page progress=%v error=%v", more, err)
		}
		if commit {
			if err := tx.Commit(ctx); err != nil {
				t.Fatal(err)
			}
		}
	}
	page(false)
	var cursor string
	var seen int64
	var initialized bool
	progress := func(wantCursor string, wantSeen int64, wantDone bool) {
		t.Helper()
		if err := pool.QueryRow(ctx, `SELECT coalesce(p.cursor,''),coalesce(p.seen,0),o.counters ? 'versions_in_scope' FROM operations o LEFT JOIN queue_operation_scope_progress p ON (p.organization,p.operation_id)=(o.organization,o.id) WHERE o.id='paged'`).Scan(&cursor, &seen, &initialized); err != nil {
			t.Fatal(err)
		}
		if cursor != wantCursor || seen != wantSeen || initialized != wantDone {
			t.Fatalf("scope progress=(%s,%d,%v), want (%s,%d,%v)", cursor, seen, initialized, wantCursor, wantSeen, wantDone)
		}
	}
	progress("", 0, false)
	for i := 2; i <= 6; i += 2 {
		page(true)
		progress(fmt.Sprintf("record-%d", i), 0, false)
	}
	page(true)
	progress("record-7", 1, true)
	var scope int64
	if err := pool.QueryRow(ctx, `SELECT (counters->>'versions_in_scope')::bigint FROM operations WHERE id='paged'`).Scan(&scope); err != nil || scope != 1 {
		t.Fatalf("final scope=%d error=%v", scope, err)
	}

	// Completed document totals supply the scope without visiting Records.
	if more, err := (CorpusStatsStore{Pool: pool}).Bootstrap(ctx, 1000); err != nil || !more {
		t.Fatalf("corpus bootstrap=%v error=%v", more, err)
	}
	exec(`INSERT INTO operations(organization,id,kind,corpus_id,request_key,canonical_request,target_generation_id) VALUES('example','rollup','projection_rebuild','corpus','rollup','','target')`)
	locked, err := pool.Begin(ctx)
	if err != nil {
		t.Fatal(err)
	}
	defer locked.Rollback(ctx)
	if _, err = locked.Exec(ctx, `LOCK records IN ACCESS EXCLUSIVE MODE`); err != nil {
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
	if more, err := advanceQueueOperationScopes(ctx, tx, 2); err != nil || !more {
		t.Fatalf("complete rollup scope visited Records: progress=%v error=%v", more, err)
	}
	if err = tx.Commit(ctx); err != nil {
		t.Fatal(err)
	}
	if err = pool.QueryRow(ctx, `SELECT (counters->>'versions_in_scope')::bigint FROM operations WHERE id='rollup'`).Scan(&scope); err != nil || scope != 1 {
		t.Fatalf("rollup scope=%d error=%v", scope, err)
	}

}
