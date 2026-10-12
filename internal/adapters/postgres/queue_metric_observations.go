package postgres

import (
	"context"

	"github.com/jackc/pgx/v5"
)

// queueMetricSources is also used by bootstrap. Keep this order stable so all
// application paths name source families consistently.
var queueMetricSources = []string{"delivery", "evaluation", "ingestion"}

// queueMetricKey identifies the primary key of one source work item. The
// sequence is zero for ingestion receipts and deliveries.
type queueMetricKey struct {
	source   string
	org      string
	id       string
	sequence int64
}

const queueMetricKeyArraysSQL = `
 SELECT DISTINCT source,org,work_id,sequence
 FROM unnest($1::text[],$2::text[],$3::text[],$4::bigint[])
   keys(source,org,work_id,sequence)`

const seedQueueMetricStripesSQL = `
 WITH touched AS (
  SELECT DISTINCT k.source,(hashtextextended(k.org,0)&63)::integer AS stripe
  FROM (` + queueMetricKeyArraysSQL + `) k
 )
 INSERT INTO queue_metric_totals(source,stripe)
 SELECT source,stripe FROM touched ORDER BY source,stripe
 ON CONFLICT(source,stripe) DO NOTHING`

const lockQueueMetricStripesSQL = `
 SELECT t.source,t.stripe
 FROM queue_metric_totals t
 WHERE EXISTS (
  SELECT 1
  FROM (` + queueMetricKeyArraysSQL + `) k
  WHERE (k.source,(hashtextextended(k.org,0)&63)::integer)=(t.source,t.stripe)
 )
 ORDER BY t.source,t.stripe
 FOR UPDATE`

// The desired CTE performs only source-primary-key point reads. It is run as a
// statement after lockQueueMetricStripesSQL, so READ COMMITTED obtains a fresh
// snapshot after any competing canonical writer releases its stripe.
const reconcileQueueMetricKeysSQL = `
 WITH keys AS MATERIALIZED (` + queueMetricKeyArraysSQL + `),
 desired AS MATERIALIZED (
  SELECT k.source,k.org,k.work_id,k.sequence,r.record_id,r.accepted_at AS admitted_at,false AS erroring
  FROM keys k
  JOIN LATERAL (
   SELECT record_id,accepted_at
   FROM ingestion_receipts
   WHERE organization=k.org AND id=k.work_id AND state='pending'
   OFFSET 0
  ) r ON true
  WHERE k.source='ingestion'
  UNION ALL
  SELECT k.source,k.org,k.work_id,k.sequence,i.record_id,i.available_at,(i.error_code<>'') AS erroring
  FROM keys k
  JOIN LATERAL (
   SELECT record_id,available_at,error_code
   FROM evaluation_intents
   WHERE organization=k.org AND subscription_version_id=k.work_id
     AND sequence=k.sequence AND state='pending'
   OFFSET 0
  ) i ON true
  WHERE k.source='evaluation'
  UNION ALL
  SELECT k.source,k.org,k.work_id,k.sequence,''::text AS record_id,coalesce(d.window_start,d.created_at),false AS erroring
  FROM keys k
  JOIN LATERAL (
   SELECT d.window_start,d.created_at
   FROM deliveries d
   JOIN delivery_outbox o ON (o.organization,o.delivery_id)=(d.organization,d.id)
   WHERE d.organization=k.org AND d.id=k.work_id
     AND o.available_at<'infinity'
     AND d.state IN ('pending','delivering')
     AND d.window_start IS DISTINCT FROM 'infinity'
   OFFSET 0
  ) d ON true
  WHERE k.source='delivery'
 ),
 old AS MATERIALIZED (
  SELECT i.ctid,i.source,i.organization,i.work_id,i.sequence,i.erroring
  FROM keys k JOIN LATERAL (
   SELECT ctid,source,organization,work_id,sequence,erroring FROM queue_metric_items
   WHERE (source,organization,work_id,sequence)=(k.source,k.org,k.work_id,k.sequence) OFFSET 0
  ) i ON true
 ),
 old_counts AS (
  SELECT source,(hashtextextended(organization,0)&63)::integer AS stripe,
    count(*) AS pending,count(*) FILTER (WHERE erroring) AS erroring
  FROM old GROUP BY source,stripe
 ),
 new_counts AS (
  SELECT source,(hashtextextended(org,0)&63)::integer AS stripe,
    count(*) AS pending,count(*) FILTER (WHERE erroring) AS erroring
  FROM desired GROUP BY source,stripe
 ),
 deltas AS (
  SELECT coalesce(n.source,o.source) AS source,
    coalesce(n.stripe,o.stripe) AS stripe,
    coalesce(n.pending,0)-coalesce(o.pending,0) AS pending,
    coalesce(n.erroring,0)-coalesce(o.erroring,0) AS erroring
  FROM old_counts o FULL JOIN new_counts n USING(source,stripe)
 ),
 adjusted AS (
  UPDATE queue_metric_totals t
  SET pending=t.pending+d.pending,erroring=t.erroring+d.erroring
  FROM deltas d
  WHERE (t.source,t.stripe)=(d.source,d.stripe)
    AND (d.pending<>0 OR d.erroring<>0)
  RETURNING t.source,t.stripe
 ),
 deleted AS (
  DELETE FROM queue_metric_items WHERE ctid=ANY(ARRAY(
   SELECT i.ctid FROM old i WHERE NOT EXISTS (
      SELECT FROM desired d
      WHERE (d.source,d.org,d.work_id,d.sequence)=(i.source,i.organization,i.work_id,i.sequence)
    ))) RETURNING source
 )
 INSERT INTO queue_metric_items(source,organization,work_id,sequence,record_id,admitted_at,erroring)
 SELECT source,org,work_id,sequence,record_id,admitted_at,erroring
 FROM desired
 ON CONFLICT(source,organization,work_id,sequence) DO UPDATE
 SET record_id=EXCLUDED.record_id,admitted_at=EXCLUDED.admitted_at,erroring=EXCLUDED.erroring
 WHERE (queue_metric_items.record_id,queue_metric_items.admitted_at,queue_metric_items.erroring)
   IS DISTINCT FROM (EXCLUDED.record_id,EXCLUDED.admitted_at,EXCLUDED.erroring)`

// queueRecordMetricObservationSQL maintains ingestion and evaluation metrics
// for the Records already fenced by queueRecordObservationSQL. Every statement
// takes the same organization and record arrays so it can be appended to that
// existing pgx batch without a round trip. The source reads are limited to
// pending rows for those Records; prior metric memberships are reached through
// queue_metric_items.record_id and are included so terminal rows are removed.
const queueRecordMetricTargetsSQL = `SELECT DISTINCT organization,record_id
 FROM unnest($1::text[],$2::text[]) keys(organization,record_id)`

var queueRecordMetricObservationSQL = []string{
	`WITH targets AS MATERIALIZED (` + queueRecordMetricTargetsSQL + `),
 wanted AS (
  SELECT DISTINCT source,(hashtextextended(t.organization,0)&63)::integer AS stripe
  FROM targets t CROSS JOIN (VALUES('evaluation'),('ingestion')) sources(source)
 )
 INSERT INTO queue_metric_totals(source,stripe)
 SELECT source,stripe FROM wanted ORDER BY source,stripe
 ON CONFLICT(source,stripe) DO NOTHING`,
	`SELECT t.source,t.stripe
 FROM queue_metric_totals t
 WHERE EXISTS (
  SELECT 1 FROM (` + queueRecordMetricTargetsSQL + `) k
  WHERE t.source IN ('evaluation','ingestion')
    AND t.stripe=(hashtextextended(k.organization,0)&63)::integer
 )
 ORDER BY t.source,t.stripe
 FOR UPDATE`,
	`WITH targets AS MATERIALIZED (` + queueRecordMetricTargetsSQL + `),
 desired AS MATERIALIZED (
  SELECT 'ingestion'::text AS source,r.organization,r.id AS work_id,0::bigint AS sequence,
    r.record_id,r.accepted_at AS admitted_at,false AS erroring
  FROM targets k
  JOIN LATERAL (
   SELECT organization,id,record_id,accepted_at
   FROM ingestion_receipts
   WHERE organization=k.organization AND record_id=k.record_id AND state='pending'
   OFFSET 0
  ) r ON true
  UNION ALL
  SELECT 'evaluation'::text AS source,i.organization,i.subscription_version_id AS work_id,i.sequence,
    i.record_id,i.available_at,(i.error_code<>'') AS erroring
  FROM targets k
  JOIN LATERAL (
   SELECT organization,subscription_version_id,sequence,record_id,available_at,error_code
   FROM evaluation_intents
   WHERE organization=k.organization AND record_id=k.record_id AND state='pending'
   OFFSET 0
  ) i ON true
 ),
 keys AS MATERIALIZED (
  SELECT DISTINCT source,organization,work_id,sequence
  FROM (
   SELECT source,organization,work_id,sequence FROM desired
   UNION ALL
   SELECT i.source,i.organization,i.work_id,i.sequence
   FROM targets k JOIN LATERAL (
    SELECT source,organization,work_id,sequence FROM queue_metric_items
    WHERE source IN ('evaluation','ingestion') AND (organization,record_id)=(k.organization,k.record_id) OFFSET 0
   ) i ON true
  ) candidates
 ),
 old AS MATERIALIZED (
  SELECT i.ctid,i.source,i.organization,i.work_id,i.sequence,i.erroring
  FROM keys k JOIN LATERAL (
   SELECT ctid,source,organization,work_id,sequence,erroring FROM queue_metric_items
   WHERE (source,organization,work_id,sequence)=(k.source,k.organization,k.work_id,k.sequence) OFFSET 0
  ) i ON true
 ),
 old_counts AS (
  SELECT source,(hashtextextended(organization,0)&63)::integer AS stripe,
    count(*) AS pending,count(*) FILTER (WHERE erroring) AS erroring
  FROM old GROUP BY source,stripe
 ),
 new_counts AS (
  SELECT source,(hashtextextended(organization,0)&63)::integer AS stripe,
    count(*) AS pending,count(*) FILTER (WHERE erroring) AS erroring
  FROM desired GROUP BY source,stripe
 ),
 deltas AS (
  SELECT coalesce(n.source,o.source) AS source,
    coalesce(n.stripe,o.stripe) AS stripe,
    coalesce(n.pending,0)-coalesce(o.pending,0) AS pending,
    coalesce(n.erroring,0)-coalesce(o.erroring,0) AS erroring
  FROM old_counts o FULL JOIN new_counts n USING(source,stripe)
 ),
 adjusted AS (
  UPDATE queue_metric_totals t
  SET pending=t.pending+d.pending,erroring=t.erroring+d.erroring
  FROM deltas d
  WHERE (t.source,t.stripe)=(d.source,d.stripe)
    AND (d.pending<>0 OR d.erroring<>0)
  RETURNING t.source,t.stripe
 ),
 deleted AS (
  DELETE FROM queue_metric_items WHERE ctid=ANY(ARRAY(
   SELECT i.ctid FROM old i WHERE NOT EXISTS (
     SELECT FROM desired d
     WHERE (d.source,d.organization,d.work_id,d.sequence)=(i.source,i.organization,i.work_id,i.sequence)
    ))) RETURNING source
 )
 INSERT INTO queue_metric_items(source,organization,work_id,sequence,record_id,admitted_at,erroring)
 SELECT source,organization,work_id,sequence,record_id,admitted_at,erroring
 FROM desired
 ON CONFLICT(source,organization,work_id,sequence) DO UPDATE
 SET record_id=EXCLUDED.record_id,admitted_at=EXCLUDED.admitted_at,erroring=EXCLUDED.erroring
 WHERE (queue_metric_items.record_id,queue_metric_items.admitted_at,queue_metric_items.erroring)
   IS DISTINCT FROM (EXCLUDED.record_id,EXCLUDED.admitted_at,EXCLUDED.erroring)`,
}

// observeQueueMetricKeys maintains metric membership for one committed batch
// of canonical source mutations. It is deliberately a batched sequence of
// separate statements: seed and lock finish before the desired CTE gets its
// fresh MVCC snapshot.
func observeQueueMetricKeys(ctx context.Context, tx pgx.Tx, keys []queueMetricKey) error {
	if len(keys) == 0 {
		return nil
	}
	batch := &pgx.Batch{}
	queueMetricObservations(batch, keys)
	return tx.SendBatch(ctx, batch).Close()
}

// queueMetricObservations appends the seed, canonical stripe lock and desired
// membership statements to an existing batch. Callers that already have a
// canonical journal/observation batch can therefore maintain metrics without
// another round trip; each queued statement still receives its own snapshot.
func queueMetricObservations(batch *pgx.Batch, keys []queueMetricKey) {
	if len(keys) == 0 {
		return
	}
	sources := make([]string, len(keys))
	orgs := make([]string, len(keys))
	ids := make([]string, len(keys))
	sequences := make([]int64, len(keys))
	for i, key := range keys {
		sources[i] = key.source
		orgs[i] = key.org
		ids[i] = key.id
		sequences[i] = key.sequence
	}
	args := []any{sources, orgs, ids, sequences}
	batch.Queue(seedQueueMetricStripesSQL, args...)
	batch.Queue(lockQueueMetricStripesSQL, args...)
	batch.Queue(reconcileQueueMetricKeysSQL, args...)
}
