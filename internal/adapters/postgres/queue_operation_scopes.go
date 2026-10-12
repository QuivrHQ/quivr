package postgres

import (
	"context"
	"github.com/jackc/pgx/v5"
)

// Scope discovery pages the corpus outside publication. The page bounds raw
// records before applying eligibility, including corpora full of ineligible
// versions. Cursor and count commit together; processing can run ahead without
// hiding undiscovered work, since incomplete scope is explicitly estimated.
func advanceQueueOperationScopes(ctx context.Context, tx pgx.Tx, limit int) (bool, error) {
	var org, id, corpus string
	err := tx.QueryRow(ctx, `SELECT organization,id,corpus_id FROM operations
 WHERE kind IN ('projection_rebuild','retrieval_configuration') AND state IN ('queued','running')
 AND NOT counters ? 'versions_in_scope' ORDER BY created_at,id LIMIT 1 FOR UPDATE SKIP LOCKED`).Scan(&org, &id, &corpus)
	if err == pgx.ErrNoRows {
		return false, nil
	}
	if err != nil {
		return false, err
	}
	if _, err = tx.Exec(ctx, `INSERT INTO queue_operation_scope_progress(organization,operation_id) VALUES($1,$2) ON CONFLICT DO NOTHING`, org, id); err != nil {
		return false, err
	}
	var cursor string
	var seen int64
	if err = tx.QueryRow(ctx, `SELECT cursor,seen FROM queue_operation_scope_progress WHERE organization=$1 AND operation_id=$2 FOR UPDATE`, org, id).Scan(&cursor, &seen); err != nil {
		return false, err
	}
	var next string
	var count, eligible int64
	err = tx.QueryRow(ctx, `SELECT coalesce(max(r.id),$3),count(*),count(*) FILTER(WHERE `+eligibleVersionPointSQL+`)
 FROM (SELECT * FROM records WHERE organization=$1 AND corpus_id=$2 AND id>$3
 ORDER BY id LIMIT $4) r
 LEFT JOIN record_versions v ON (v.organization,v.id)=(r.organization,r.current_version_id)`, org, corpus, cursor, limit).Scan(&next, &count, &eligible)
	if err != nil {
		return false, err
	}
	seen += eligible
	if _, err = tx.Exec(ctx, `UPDATE queue_operation_scope_progress SET cursor=$3,seen=$4 WHERE organization=$1 AND operation_id=$2`, org, id, next, seen); err != nil {
		return false, err
	}
	if count < int64(limit) {
		_, err = tx.Exec(ctx, `UPDATE operations SET counters=counters || jsonb_build_object('versions_in_scope',$3::bigint)
 WHERE organization=$1 AND id=$2 AND state IN ('queued','running') AND NOT counters ? 'versions_in_scope'`, org, id, seen)
	}
	// A later turn also discovers other operations; no scan is tied to refresh pacing.
	return true, err
}
