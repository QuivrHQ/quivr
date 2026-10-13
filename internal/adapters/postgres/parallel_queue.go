package postgres

import (
	"context"
	"errors"
	"sort"

	"github.com/jackc/pgx/v5"
)

// parallelQueueRecord is read without a row lock. A producer can therefore
// advance the dirty revision while reconciliation waits for an aggregate stripe
// or a Record observation row; the final acknowledgement is a revision CAS.
type parallelQueueRecord struct {
	organization string
	record       string
	revision     int64
}

// ReconcileParallelQueue drains at most limit dirty Records. It is the bounded
// production hook used by QueueSnapshots.Maintain and is also useful to a
// deployment's explicit maintenance loop. Aggregate stripes are acquired
// before any contribution or Record observation locks.
func (s QueueSnapshots) ReconcileParallelQueue(ctx context.Context, limit int) (bool, error) {
	if s.Pool == nil {
		return false, errors.New("workqueue: nil postgres pool")
	}
	if limit <= 0 {
		return false, nil
	}
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return false, err
	}
	defer tx.Rollback(ctx)
	more, err := ReconcileParallelQueueTx(ctx, tx, limit)
	if err != nil {
		return false, err
	}
	if err = tx.Commit(ctx); err != nil {
		return false, err
	}
	return more, nil
}

// ReconcileParallelQueueTx drains at most limit dirty Records in tx. The
// caller can use this while holding another transaction-scoped cutover fence,
// such as journalModeLock. It also takes the maintenance lock, so a cutover
// cannot race QueueSnapshots.Maintain or another explicit drain.
func ReconcileParallelQueueTx(ctx context.Context, tx pgx.Tx, limit int) (bool, error) {
	if tx == nil {
		return false, errors.New("workqueue: nil postgres transaction")
	}
	if limit <= 0 {
		return false, nil
	}
	var locked bool
	if err := tx.QueryRow(ctx, `SELECT pg_try_advisory_xact_lock($1)`, queueMaintenanceLock).Scan(&locked); err != nil {
		return false, err
	}
	if !locked {
		return false, nil
	}
	return advanceParallelQueueObservations(ctx, tx, limit)
}

func advanceParallelQueueObservations(ctx context.Context, tx pgx.Tx, limit int) (bool, error) {
	if limit <= 0 {
		return false, nil
	}
	rows, err := tx.Query(ctx, `SELECT organization,record_id,revision
 FROM parallel_queue_observations
 WHERE revision<>applied_revision
 ORDER BY organization,record_id
 LIMIT $1`, limit)
	if err != nil {
		return false, err
	}
	dirty := make([]parallelQueueRecord, 0, limit)
	for rows.Next() {
		var item parallelQueueRecord
		if err = rows.Scan(&item.organization, &item.record, &item.revision); err != nil {
			rows.Close()
			return false, err
		}
		dirty = append(dirty, item)
	}
	if err = rows.Err(); err != nil {
		rows.Close()
		return false, err
	}
	rows.Close()
	if len(dirty) == 0 {
		return false, nil
	}
	if err = reconcileParallelQueueRecords(ctx, tx, dirty); err != nil {
		return false, err
	}
	if len(dirty) < limit {
		return false, nil
	}
	var more bool
	err = tx.QueryRow(ctx, `SELECT EXISTS(SELECT FROM parallel_queue_observations WHERE revision<>applied_revision)`).Scan(&more)
	return more, err
}

// reconcileParallelQueueKeys is used by maintenance paths that already found
// a bounded set of Records. It folds any currently dirty revision into the
// same transaction, so periodic bootstrap does not increment its own dirty
// rows forever.
func reconcileParallelQueueKeys(ctx context.Context, tx pgx.Tx, organizations, records []string) error {
	if len(organizations) != len(records) {
		return errors.New("workqueue: mismatched queue observation keys")
	}
	keys := make(map[[2]string]bool, len(records))
	for i, record := range records {
		if organizations[i] == "" || record == "" {
			continue
		}
		keys[[2]string{organizations[i], record}] = true
	}
	if len(keys) == 0 {
		return nil
	}
	orgs := make([]string, 0, len(keys))
	ids := make([]string, 0, len(keys))
	for key := range keys {
		orgs = append(orgs, key[0])
		ids = append(ids, key[1])
	}
	orderParallelQueueKeys(orgs, ids)
	rows, err := tx.Query(ctx, `SELECT organization,record_id,revision
 FROM parallel_queue_observations
 WHERE (organization,record_id) IN (SELECT * FROM unnest($1::text[],$2::text[]))
   AND revision<>applied_revision
 ORDER BY organization,record_id`, orgs, ids)
	if err != nil {
		return err
	}
	dirty := make([]parallelQueueRecord, 0, len(keys))
	for rows.Next() {
		var item parallelQueueRecord
		if err = rows.Scan(&item.organization, &item.record, &item.revision); err != nil {
			rows.Close()
			return err
		}
		dirty = append(dirty, item)
	}
	if err = rows.Err(); err != nil {
		rows.Close()
		return err
	}
	rows.Close()
	for key := range keys {
		found := false
		for _, item := range dirty {
			if item.organization == key[0] && item.record == key[1] {
				found = true
				break
			}
		}
		if !found {
			dirty = append(dirty, parallelQueueRecord{organization: key[0], record: key[1]})
		}
	}
	return reconcileParallelQueueRecords(ctx, tx, dirty)
}

func orderParallelQueueKeys(organizations, records []string) {
	order := make([]int, len(records))
	for i := range order {
		order[i] = i
	}
	sort.Slice(order, func(i, j int) bool {
		left, right := order[i], order[j]
		if organizations[left] == organizations[right] {
			return records[left] < records[right]
		}
		return organizations[left] < organizations[right]
	})
	orderedOrganizations := make([]string, len(order))
	orderedRecords := make([]string, len(order))
	for i, index := range order {
		orderedOrganizations[i], orderedRecords[i] = organizations[index], records[index]
	}
	copy(organizations, orderedOrganizations)
	copy(records, orderedRecords)
}

func reconcileParallelQueueRecords(ctx context.Context, tx pgx.Tx, dirty []parallelQueueRecord) error {
	if len(dirty) == 0 {
		return nil
	}
	orgs, records := make([]string, 0, len(dirty)), make([]string, 0, len(dirty))
	seen := make(map[[2]string]bool, len(dirty))
	for _, item := range dirty {
		if item.organization == "" || item.record == "" {
			continue
		}
		key := [2]string{item.organization, item.record}
		if seen[key] {
			continue
		}
		seen[key] = true
		orgs = append(orgs, item.organization)
		records = append(records, item.record)
	}
	if len(orgs) == 0 {
		return nil
	}
	orderParallelQueueKeys(orgs, records)
	if err := lockParallelQueueAggregates(ctx, tx, orgs); err != nil {
		return err
	}

	// Aggregate stripes are held before this batch takes queue_enrichment or
	// corpus observation locks. Every subsequent statement has a fresh READ
	// COMMITTED snapshot after any producer waiting on canonical state commits.
	canonical := &pgx.Batch{}
	queueRecordCanonicalObservations(canonical, orgs, records, true)
	if err := tx.SendBatch(ctx, canonical).Close(); err != nil {
		return err
	}

	backlog := &pgx.Batch{}
	backlog.Queue(forceParallelQueueSQL(queueRecordObservationSQL[2]), orgs, records)
	if err := tx.SendBatch(ctx, backlog).Close(); err != nil {
		return err
	}

	metricKeys, err := collectParallelQueueMetricKeys(ctx, tx, orgs, records)
	if err != nil {
		return err
	}
	if len(metricKeys) > 0 {
		metric := &pgx.Batch{}
		metric.Queue(forceParallelQueueSQL(reconcileQueueMetricKeysSQL), parallelQueueMetricArgs(metricKeys)...)
		if err = tx.SendBatch(ctx, metric).Close(); err != nil {
			return err
		}
	}

	derived := &pgx.Batch{}
	queueCorpusRecordObservations(derived, orgs, records)
	for _, item := range dirty {
		if item.revision <= 0 {
			continue
		}
		derived.Queue(`UPDATE parallel_queue_observations
 SET applied_revision=$3
 WHERE organization=$1 AND record_id=$2 AND revision=$3 AND applied_revision<=$3`, item.organization, item.record, item.revision)
	}
	return tx.SendBatch(ctx, derived).Close()
}

func lockParallelQueueAggregates(ctx context.Context, tx pgx.Tx, organizations []string) error {
	if _, err := tx.Exec(ctx, `INSERT INTO queue_backlog_totals(stripe,queue)
 SELECT DISTINCT (hashtextextended(o,0)&63)::integer,q
 FROM unnest($1::text[]) orgs(o) CROSS JOIN (VALUES('live'),('bulk')) queues(q)
 ORDER BY 1,2 ON CONFLICT DO NOTHING`, organizations); err != nil {
		return err
	}
	rows, err := tx.Query(ctx, `SELECT stripe,queue FROM queue_backlog_totals
 WHERE stripe IN (SELECT DISTINCT (hashtextextended(o,0)&63)::integer FROM unnest($1::text[]) orgs(o))
 ORDER BY stripe,queue FOR UPDATE`, organizations)
	if err != nil {
		return err
	}
	for rows.Next() {
	}
	if err = rows.Err(); err != nil {
		return err
	}
	if _, err = tx.Exec(ctx, `INSERT INTO queue_metric_totals(source,stripe)
 SELECT source,(hashtextextended(o,0)&63)::integer
 FROM unnest($1::text[]) orgs(o) CROSS JOIN unnest($2::text[]) sources(source)
 ORDER BY source,2 ON CONFLICT DO NOTHING`, organizations, queueMetricSources); err != nil {
		return err
	}
	rows, err = tx.Query(ctx, `SELECT source,stripe FROM queue_metric_totals
 WHERE stripe IN (SELECT DISTINCT (hashtextextended(o,0)&63)::integer FROM unnest($1::text[]) orgs(o))
 ORDER BY source,stripe FOR UPDATE`, organizations)
	if err != nil {
		return err
	}
	for rows.Next() {
	}
	return rows.Err()
}

func collectParallelQueueMetricKeys(ctx context.Context, tx pgx.Tx, organizations, records []string) ([]queueMetricKey, error) {
	rows, err := tx.Query(ctx, `WITH targets AS MATERIALIZED (
 SELECT DISTINCT organization,record_id FROM unnest($1::text[],$2::text[]) keys(organization,record_id)
), keys AS (
 SELECT 'ingestion'::text AS source,r.organization,r.id AS work_id,0::bigint AS sequence
 FROM targets t JOIN ingestion_receipts r ON (r.organization,r.record_id)=(t.organization,t.record_id)
 UNION ALL
 SELECT 'evaluation'::text,i.organization,i.subscription_version_id,i.sequence
 FROM targets t JOIN evaluation_intents i ON (i.organization,i.record_id)=(t.organization,t.record_id)
 UNION ALL
 SELECT 'delivery'::text,d.organization,d.id,0::bigint
 FROM targets t JOIN matches m ON (m.organization,m.record_id)=(t.organization,t.record_id)
 JOIN deliveries d ON (d.organization,d.match_id)=(m.organization,m.id)
 UNION ALL
 SELECT i.source,i.organization,i.work_id,i.sequence
 FROM targets t JOIN queue_metric_items i ON (i.organization,i.record_id)=(t.organization,t.record_id)
)
 SELECT DISTINCT source,organization,work_id,sequence FROM keys
 ORDER BY source,organization,work_id,sequence`, organizations, records)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	keys := make([]queueMetricKey, 0)
	for rows.Next() {
		var key queueMetricKey
		if err = rows.Scan(&key.source, &key.org, &key.id, &key.sequence); err != nil {
			return nil, err
		}
		keys = append(keys, key)
	}
	return keys, rows.Err()
}

func parallelQueueMetricArgs(keys []queueMetricKey) []any {
	sources := make([]string, len(keys))
	orgs := make([]string, len(keys))
	ids := make([]string, len(keys))
	sequences := make([]int64, len(keys))
	for i, key := range keys {
		sources[i], orgs[i], ids[i], sequences[i] = key.source, key.org, key.id, key.sequence
	}
	return []any{sources, orgs, ids, sequences}
}
