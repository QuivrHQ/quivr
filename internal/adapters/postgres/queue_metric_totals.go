package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

// Metric totals retain their work-item units and initialization state. A read
// never scans source work; the arrival index visits at most one pending item.
func queueMetricBacklog(ctx context.Context, pool *pgxpool.Pool, source string) (pending, erroring int64, age float64, err error) {
	err = pool.QueryRow(ctx, `SELECT coalesce(sum(t.pending),0)::bigint,coalesce(sum(t.erroring),0)::bigint,
	coalesce(extract(epoch FROM statement_timestamp()-(SELECT admitted_at FROM queue_metric_items WHERE source=$1 ORDER BY admitted_at LIMIT 1)),0)::double precision
	 FROM queue_metric_bootstrap b LEFT JOIN queue_metric_totals t ON t.source=b.source
	 WHERE b.source=$1 AND b.initialized
	 AND NOT EXISTS(SELECT FROM parallel_queue_observations WHERE revision<>applied_revision AND dirty_since<=statement_timestamp()-interval '1 minute')
	 AND ($1<>'delivery' OR NOT EXISTS(SELECT FROM queue_scope_reconciliation WHERE kind='delivery')) GROUP BY b.source`, source).Scan(&pending, &erroring, &age)
	return
}

type queueMetricBootstrapState struct {
	source      string
	org         string
	id          string
	sequence    int64
	initialized bool
	active      bool
	keys        []queueMetricKey
}

// queueMetricBootstrapPageSQL keeps the source and stored-item streams
// independently bounded before they are merged. This prevents a large stream
// of old metric items from starving canonical source rows (or vice versa).
func queueMetricBootstrapPageSQL(source string) string {
	const prefix = `WITH canonical AS MATERIALIZED (`
	const suffix = `), stored AS MATERIALIZED (
 SELECT organization,work_id,sequence
 FROM queue_metric_items
 WHERE source='%s' AND (organization,work_id,sequence)>($1,$2,$3)
 ORDER BY organization,work_id,sequence LIMIT $4
)
SELECT organization,work_id,sequence FROM (
 SELECT organization,work_id,sequence FROM canonical
 UNION
 SELECT organization,work_id,sequence FROM stored
) keys
ORDER BY organization,work_id,sequence LIMIT $4`
	switch source {
	case "delivery":
		return prefix + `
 SELECT organization,id AS work_id,0::bigint AS sequence
 FROM deliveries
 WHERE (organization,id)>($1,$2)
 ORDER BY organization,id
		LIMIT $4` + "\n" + fmt.Sprintf(suffix, source)
	case "evaluation":
		return prefix + `
 SELECT organization,subscription_version_id AS work_id,sequence
 FROM evaluation_intents
 WHERE (organization,subscription_version_id,sequence)>($1,$2,$3)
 ORDER BY organization,subscription_version_id,sequence
		LIMIT $4` + "\n" + fmt.Sprintf(suffix, source)
	case "ingestion":
		return prefix + `
 SELECT organization,id AS work_id,0::bigint AS sequence
 FROM ingestion_receipts
 WHERE (organization,id)>($1,$2)
 ORDER BY organization,id
		LIMIT $4` + "\n" + fmt.Sprintf(suffix, source)
	default:
		panic("unknown queue metric source: " + source)
	}
}

func collectQueueMetricBootstrapPage(ctx context.Context, tx pgx.Tx, source, org, id string, sequence int64, limit int) ([]queueMetricKey, error) {
	rows, err := tx.Query(ctx, queueMetricBootstrapPageSQL(source), org, id, sequence, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	keys := make([]queueMetricKey, 0, limit)
	for rows.Next() {
		var key queueMetricKey
		key.source = source
		if err := rows.Scan(&key.org, &key.id, &key.sequence); err != nil {
			return nil, err
		}
		keys = append(keys, key)
	}
	return keys, rows.Err()
}

func ensureQueueMetricState(ctx context.Context, tx pgx.Tx) error {
	if _, err := tx.Exec(ctx, `INSERT INTO queue_metric_bootstrap(source)
 SELECT source FROM unnest($1::text[]) sources(source)
 ON CONFLICT(source) DO NOTHING`, queueMetricSources); err != nil {
		return err
	}
	_, err := tx.Exec(ctx, `WITH wanted AS (
	 SELECT source,stripe FROM unnest($1::text[]) sources(source)
	 CROSS JOIN generate_series(0,63) stripes(stripe)
	 ORDER BY source,stripe
 )
 INSERT INTO queue_metric_totals(source,stripe)
	 SELECT source,stripe FROM wanted
	 ON CONFLICT(source,stripe) DO NOTHING`, queueMetricSources)
	return err
}

// advanceQueueMetricBootstrap initializes each source in resumable keyset
// pages. Once initialized, the same page mechanism runs again every five
// minutes so writers predating application observation cannot leave stale
// membership behind. Stored metric keys are paged along with canonical rows,
// which also removes memberships whose source row was deleted.
func advanceQueueMetricBootstrap(ctx context.Context, tx pgx.Tx, limit int) (more bool, err error) {
	if limit <= 0 {
		return false, nil
	}
	if err = ensureQueueMetricState(ctx, tx); err != nil {
		return false, err
	}

	states := make([]queueMetricBootstrapState, 0, len(queueMetricSources))
	var observed []queueMetricKey
	for _, source := range queueMetricSources {
		state := queueMetricBootstrapState{source: source}
		var due bool
		if err = tx.QueryRow(ctx, `SELECT organization,work_id,sequence,initialized,
 (next_run<=statement_timestamp()) AS due
 FROM queue_metric_bootstrap WHERE source=$1 FOR UPDATE`, source).
			Scan(&state.org, &state.id, &state.sequence, &state.initialized, &due); err != nil {
			return false, err
		}
		if state.initialized && !due {
			states = append(states, state)
			continue
		}

		state.active = true
		state.keys, err = collectQueueMetricBootstrapPage(ctx, tx, source, state.org, state.id, state.sequence, limit)
		if err != nil {
			return false, err
		}
		observed = append(observed, state.keys...)
		states = append(states, state)
	}

	// All bootstrap rows are selected before this call acquires any metric
	// stripe. Thus the transaction never holds a stripe while reaching for the
	// next source's bootstrap lock.
	if len(observed) > 0 {
		if err = observeQueueMetricKeysForced(ctx, tx, observed); err != nil {
			return false, err
		}
	}

	for _, state := range states {
		if !state.active {
			continue
		}
		if len(state.keys) < limit {
			if _, err = tx.Exec(ctx, `UPDATE queue_metric_bootstrap
 SET organization='',work_id='',sequence=0,initialized=true,
     next_run=statement_timestamp()+interval '5 minutes'
 WHERE source=$1`, state.source); err != nil {
				return false, err
			}
			continue
		}
		last := state.keys[len(state.keys)-1]
		if _, err = tx.Exec(ctx, `UPDATE queue_metric_bootstrap
 SET organization=$2,work_id=$3,sequence=$4
 WHERE source=$1`, state.source, last.org, last.id, last.sequence); err != nil {
			return false, err
		}
		more = true
	}
	return more, nil
}
