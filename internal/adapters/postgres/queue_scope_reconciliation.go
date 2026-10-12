package postgres

import (
	"context"
	"github.com/jackc/pgx/v5"
)

// Scope transitions hold only a durable request. Every maintenance turn bounds
// raw source rows before eligibility, then observes the selected keys in a new
// statement snapshot. Publication cannot expose a partly repaired scope.
func advanceQueueScopeReconciliation(ctx context.Context, tx pgx.Tx, limit int) (bool, error) {
	var kind, org, resource, cursor string
	err := tx.QueryRow(ctx, `SELECT kind,organization,resource_id,cursor FROM queue_scope_reconciliation
 ORDER BY kind,organization,resource_id LIMIT 1 FOR UPDATE SKIP LOCKED`).Scan(&kind, &org, &resource, &cursor)
	if err == pgx.ErrNoRows {
		return false, nil
	}
	if err != nil {
		return false, err
	}
	var rows pgx.Rows
	if kind == "quarantine" {
		rows, err = tx.Query(ctx, `SELECT version_id,record_id,true FROM quarantine_reprocess_items
 WHERE organization=$1 AND operation_id=$2 AND version_id>$3 ORDER BY version_id LIMIT $4`, org, resource, cursor, limit)
	} else {
		// Bound the Organization's raw primary-key page before checking the
		// subscription. Sparse scopes must not turn a page into an unbounded scan.
		rows, err = tx.Query(ctx, `SELECT d.id,''::text,coalesce(m.subscription_id=$2,false)
 FROM (SELECT id,match_id FROM deliveries WHERE organization=$1 AND id>$3 ORDER BY id LIMIT $4) d
 LEFT JOIN matches m ON (m.organization,m.id)=($1,d.match_id) ORDER BY d.id`, org, resource, cursor, limit)
	}
	if err != nil {
		return false, err
	}
	var records []string
	var metrics []queueMetricKey
	var n int
	for rows.Next() {
		var id, record string
		var eligible bool
		if err = rows.Scan(&id, &record, &eligible); err != nil {
			rows.Close()
			return false, err
		}
		n++
		cursor = id
		if eligible {
			if kind == "quarantine" {
				records = append(records, record)
			} else {
				metrics = append(metrics, queueMetricKey{source: "delivery", org: org, id: id})
			}
		}
	}
	rows.Close()
	if err = rows.Err(); err != nil {
		return false, err
	}
	if kind == "quarantine" {
		orgs := make([]string, len(records))
		for i := range orgs {
			orgs[i] = org
		}
		err = observeQueueRecords(ctx, tx, orgs, records)
	} else {
		err = observeQueueMetricKeys(ctx, tx, metrics)
	}
	if err != nil {
		return false, err
	}
	if n < limit {
		_, err = tx.Exec(ctx, `DELETE FROM queue_scope_reconciliation WHERE (kind,organization,resource_id)=($1,$2,$3)`, kind, org, resource)
	} else {
		_, err = tx.Exec(ctx, `UPDATE queue_scope_reconciliation SET cursor=$4 WHERE (kind,organization,resource_id)=($1,$2,$3)`, kind, org, resource, cursor)
	}
	return true, err
}
