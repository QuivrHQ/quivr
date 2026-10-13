package postgres

import (
	"context"
	"errors"
	"time"

	"github.com/jackc/pgx/v5"
)

const queueMaintenanceLock int64 = 642005 // Armada reservation, THE-1407.
const queueMaintenancePage = 1000

// Reconciliation repairs writes from previous binaries after a bounded pass.
const queueReconciliationInterval = 5 * time.Minute

// Maintain advances bounded pages of queue initialization, scheduled
// eligibility, scope discovery and attempt cleanup. More means another turn can
// make progress immediately; ordinary publication never performs this work.
func (s QueueSnapshots) Maintain(ctx context.Context) (more bool, err error) {
	if s.Pool == nil {
		return false, errors.New("workqueue: nil postgres pool")
	}
	steps := []func(context.Context, pgx.Tx) (bool, error){
		func(ctx context.Context, tx pgx.Tx) (bool, error) {
			_, err := tx.Exec(ctx, `INSERT INTO queue_backlog_totals(stripe,queue)
 SELECT s,q FROM generate_series(0,63) s CROSS JOIN (VALUES('live'),('bulk')) queues(q)
 ORDER BY s,q ON CONFLICT DO NOTHING`)
			return false, err
		},
		func(ctx context.Context, tx pgx.Tx) (bool, error) {
			if err := advanceQueueObservations(ctx, tx, queueMaintenancePage); err != nil {
				return false, err
			}
			var more bool
			err := tx.QueryRow(ctx, `SELECT NOT initialized FROM queue_enrichment_bootstrap WHERE singleton`).Scan(&more)
			return more, err
		},
		func(ctx context.Context, tx pgx.Tx) (bool, error) {
			return advanceQueueBacklogBootstrap(ctx, tx, queueMaintenancePage)
		},
		func(ctx context.Context, tx pgx.Tx) (bool, error) {
			return advanceQueueScopeReconciliation(ctx, tx, queueMaintenancePage)
		},
		advanceDueQueueDocuments,
		func(ctx context.Context, tx pgx.Tx) (bool, error) {
			return advanceQueueOperationScopes(ctx, tx, queueMaintenancePage)
		},
		func(ctx context.Context, tx pgx.Tx) (bool, error) {
			return advanceQueueMetricBootstrap(ctx, tx, queueMaintenancePage)
		},
		func(ctx context.Context, tx pgx.Tx) (bool, error) {
			tag, err := tx.Exec(ctx, `DELETE FROM queue_document_attempts WHERE (organization,kind,work_id,document_id) IN (
 SELECT organization,kind,work_id,document_id FROM queue_document_attempts
 WHERE lease_until<statement_timestamp() LIMIT 1000 FOR UPDATE SKIP LOCKED)`)
			return tag.RowsAffected() == 1000, err
		},
	}
	for _, step := range steps {
		tx, err := s.Pool.Begin(ctx)
		if err != nil {
			return more, err
		}
		var locked bool
		if err = tx.QueryRow(ctx, `SELECT pg_try_advisory_xact_lock($1)`, queueMaintenanceLock).Scan(&locked); err != nil || !locked {
			tx.Rollback(ctx)
			if err != nil {
				return more, err
			}
			continue
		}
		progress, err := step(ctx, tx)
		if err != nil {
			tx.Rollback(ctx)
			return more, err
		}
		if err = tx.Commit(ctx); err != nil {
			return more, err
		}
		more = more || progress
	}
	return more, nil
}

// Each page commits before acquiring another page's record locks. Holding
// counter locks while reaching for new record locks would invert writer order.
func advanceDueQueueDocuments(ctx context.Context, tx pgx.Tx) (bool, error) {
	rows, err := tx.Query(ctx, `SELECT organization,record_id FROM queue_backlog_documents
 WHERE NOT ready AND ready_at<=statement_timestamp() ORDER BY ready_at,organization,record_id LIMIT $1`, queueMaintenancePage)
	if err != nil {
		return false, err
	}
	keys, err := collectQueueKeys(rows)
	if err != nil || len(keys.records) == 0 {
		return false, err
	}
	err = observeQueueStateRecords(ctx, tx, keys.organizations, keys.records)
	return true, err
}

type queueKeys struct{ organizations, records []string }

func collectQueueKeys(rows pgx.Rows) (keys queueKeys, err error) {
	defer rows.Close()
	seen := make(map[[2]string]bool)
	for rows.Next() {
		var org, record string
		if err = rows.Scan(&org, &record); err != nil {
			return keys, err
		}
		key := [2]string{org, record}
		if !seen[key] {
			seen[key] = true
			keys.organizations = append(keys.organizations, org)
			keys.records = append(keys.records, record)
		}
	}
	return keys, rows.Err()
}

func advanceQueueBacklogBootstrap(ctx context.Context, tx pgx.Tx, limit int) (bool, error) {
	if _, err := tx.Exec(ctx, `INSERT INTO queue_backlog_bootstrap(singleton) VALUES(true) ON CONFLICT DO NOTHING`); err != nil {
		return false, err
	}
	var org, record string
	var initialized, due bool
	if err := tx.QueryRow(ctx, `SELECT organization,record_id,initialized,next_run<=statement_timestamp() FROM queue_backlog_bootstrap WHERE singleton FOR UPDATE`).Scan(&org, &record, &initialized, &due); err != nil || !due {
		return false, err
	}
	// Both candidate streams are bounded before union/deduplication. Fences also
	// retain keys for Records deleted by a previous binary, so reconciliation can
	// remove obsolete queue memberships without a full ledger scan.
	rows, err := tx.Query(ctx, `SELECT organization,id FROM (
  (SELECT organization,id FROM records WHERE (organization,id)>($1,$2) ORDER BY organization,id LIMIT $3)
  UNION
  (SELECT organization,record_id FROM queue_enrichment_records WHERE (organization,record_id)>($1,$2) ORDER BY organization,record_id LIMIT $3)
 ) candidates ORDER BY organization,id LIMIT $3`, org, record, limit)
	if err != nil {
		return false, err
	}
	keys, err := collectQueueKeys(rows)
	if err != nil {
		return false, err
	}
	if len(keys.records) > 0 {
		if err := observeQueueStateRecords(ctx, tx, keys.organizations, keys.records); err != nil {
			return false, err
		}
		last := len(keys.records) - 1
		org, record = keys.organizations[last], keys.records[last]
	}
	complete := len(keys.records) < limit
	if complete {
		org, record = "", ""
		initialized = true
	}
	_, err = tx.Exec(ctx, `UPDATE queue_backlog_bootstrap SET organization=$1,record_id=$2,initialized=$3,
 next_run=CASE WHEN $4 THEN statement_timestamp()+make_interval(secs=>$5::double precision) ELSE '-infinity' END WHERE singleton`, org, record, initialized, complete, queueReconciliationInterval.Seconds())
	return !complete, err
}
