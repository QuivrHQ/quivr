package postgres

import (
	"context"
	"github.com/jackc/pgx/v5"
)

// Intent transitions update both the deduplicated document queues and the raw
// evaluation gauge. Read canonical identity, rather than relying on claim fields.
func observeQueueIntents(ctx context.Context, tx pgx.Tx, org string, versions []string, sequences []int64) error {
	rows, err := tx.Query(ctx, `SELECT DISTINCT i.organization,i.record_id FROM unnest($2::text[],$3::bigint[]) keys(id,sequence)
 JOIN LATERAL (SELECT organization,record_id FROM evaluation_intents WHERE organization=$1 AND subscription_version_id=keys.id AND sequence=keys.sequence OFFSET 0) i ON true`, org, versions, sequences)
	if err != nil {
		return err
	}
	keys, err := collectQueueKeys(rows)
	if err != nil {
		return err
	}
	return observeQueueStateRecords(ctx, tx, keys.organizations, keys.records)
}
