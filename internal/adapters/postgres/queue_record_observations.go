package postgres

// Queue memberships are derived from the affected Records after their canonical
// writes. Separate statements take a fresh snapshot after observation/counter
// locks; the existing journal batch supplies both arguments and deduplicates work.
var queueRecordObservationSQL = []string{
	`INSERT INTO queue_backlog_totals(stripe,queue)
 SELECT DISTINCT (hashtextextended(o,0)&63)::integer AS stripe,q
 FROM unnest($1::text[],$2::text[]) orgs(o,r) CROSS JOIN (VALUES('live'),('bulk')) queues(q)
 ORDER BY stripe,q ON CONFLICT DO NOTHING`,
	`SELECT stripe FROM queue_backlog_totals
 WHERE stripe IN (SELECT DISTINCT (hashtextextended(o,0)&63)::integer FROM unnest($1::text[],$2::text[]) orgs(o,r))
 ORDER BY stripe,queue FOR UPDATE`,
	`WITH keys AS MATERIALIZED (SELECT DISTINCT o AS organization,r AS record_id FROM unnest($1::text[],$2::text[]) k(o,r)),
 eligible AS MATERIALIZED (
  SELECT k.* FROM keys k JOIN LATERAL (
   SELECT withdrawn FROM records WHERE (organization,id)=(k.organization,k.record_id) OFFSET 0
  ) r ON NOT r.withdrawn
  WHERE NOT COALESCE((SELECT true FROM tombstones t WHERE (t.organization,t.record_id)=(k.organization,k.record_id)),false)
 ), work AS (
  SELECT k.organization,k.record_id,CASE WHEN rc.work_queue='bulk' THEN 'bulk' ELSE 'live' END AS queue,
   coalesce(nullif(rc.version_id,''),ar.version_id,rc.id) AS document_id,
   coalesce(least(rc.accepted_at,ar.accepted_at),rc.accepted_at,ar.accepted_at) AS admitted_at,
   true AS ingestion,'-infinity'::timestamptz AS ready_at
  FROM eligible k JOIN LATERAL (
   SELECT * FROM ingestion_receipts WHERE (organization,record_id)=(k.organization,k.record_id)
   AND route_family='ingestion' AND state='pending' OFFSET 0
  ) rc ON true
  LEFT JOIN accepted_revisions ar ON (ar.organization,ar.record_id,ar.slot)=(rc.organization,rc.record_id,rc.slot)
  UNION ALL
  SELECT k.organization,k.record_id,CASE WHEN rc.work_queue='bulk' THEN 'bulk' ELSE 'live' END,v.id,
   coalesce(least(rc.accepted_at,ar.accepted_at),rc.accepted_at,ar.accepted_at),NOT v.baseline_ready,'-infinity'
  FROM eligible k JOIN LATERAL (
   SELECT * FROM record_versions WHERE (organization,record_id)=(k.organization,k.record_id)
   AND NOT baseline_ready AND NOT quarantined AND processing IN ('queued','running','retrying')
   UNION ALL
   SELECT v.* FROM records r JOIN record_versions v ON (v.organization,v.id)=(r.organization,r.current_version_id)
   WHERE (r.organization,r.id)=(k.organization,k.record_id) AND v.baseline_ready AND NOT v.quarantined
   AND v.record_id=r.id AND v.enrichment_state IN ('queued','running','retrying') OFFSET 0
  ) v ON true
  JOIN accepted_revisions ar ON (ar.organization,ar.record_id,ar.slot)=(v.organization,v.record_id,v.slot)
  LEFT JOIN ingestion_receipts rc ON (rc.organization,rc.record_id,rc.acceptance_order)=(v.organization,v.record_id,v.acceptance_order)
  UNION ALL
  SELECT k.organization,k.record_id,CASE WHEN e.work_queue='bulk' THEN 'bulk' ELSE 'live' END,e.version_id,e.created_at,false,'-infinity'
  FROM eligible k JOIN LATERAL (
   SELECT * FROM ingestion_evaluations WHERE (organization,record_id)=(k.organization,k.record_id) AND state='queued' OFFSET 0
  ) e ON true JOIN record_versions v ON (v.organization,v.id)=(e.organization,e.version_id)
  UNION ALL
  SELECT k.organization,k.record_id,CASE WHEN p.work_queue='bulk' THEN 'bulk' ELSE 'live' END,p.version_id,p.created_at,false,'-infinity'
  FROM eligible k JOIN LATERAL (
   SELECT * FROM serving_projections WHERE (organization,record_id)=(k.organization,k.record_id) AND state='queued' OFFSET 0
  ) p ON true JOIN record_versions v ON (v.organization,v.id)=(p.organization,p.version_id)
  UNION ALL
  SELECT k.organization,k.record_id,'live',i.record_version_id,i.available_at,false,i.available_at
  FROM eligible k JOIN LATERAL (
   SELECT * FROM evaluation_intents WHERE (organization,record_id)=(k.organization,k.record_id)
   AND kind='evaluation' AND state='pending' OFFSET 0
  ) i ON true JOIN record_versions v ON (v.organization,v.id)=(i.organization,i.record_version_id)
  UNION ALL
  SELECT k.organization,k.record_id,'bulk',i.version_id,o.created_at,false,'-infinity'
  FROM eligible k JOIN LATERAL (
   SELECT * FROM quarantine_reprocess_items WHERE (organization,record_id)=(k.organization,k.record_id)
   AND phase IN ('pending','renormalizing','released') OFFSET 0
  ) i ON true JOIN operations o ON (o.organization,o.id)=(i.organization,i.operation_id)
  WHERE o.kind='quarantine_reprocess' AND o.state IN ('queued','running')
 )
, desired(organization,record_id,queue,document_id,admitted_at,ingestion,ready_at,ready) AS MATERIALIZED (SELECT organization,record_id,queue,document_id,
  coalesce(min(admitted_at) FILTER(WHERE ready_at<=statement_timestamp()),min(admitted_at)),
  bool_or(ingestion),min(ready_at),min(ready_at)<=statement_timestamp()
 FROM work WHERE document_id<>'' GROUP BY organization,record_id,queue,document_id),
old_counts AS (
  SELECT (hashtextextended(d.organization,0)&63)::integer AS stripe,d.queue,
   count(*) FILTER(WHERE d.ready) AS pending,count(*) FILTER(WHERE d.ready AND d.ingestion) AS ingestion
  FROM keys k JOIN LATERAL (
   SELECT * FROM queue_backlog_documents WHERE (organization,record_id)=(k.organization,k.record_id) OFFSET 0
  ) d ON true GROUP BY stripe,d.queue
 ), new_counts AS (
  SELECT (hashtextextended(organization,0)&63)::integer AS stripe,queue,
   count(*) FILTER(WHERE ready) AS pending,count(*) FILTER(WHERE ready AND ingestion) AS ingestion
  FROM desired GROUP BY stripe,queue
 ), deltas AS (
  SELECT coalesce(n.stripe,o.stripe) AS stripe,coalesce(n.queue,o.queue) AS queue,
   coalesce(n.pending,0)-coalesce(o.pending,0) AS pending,
   coalesce(n.ingestion,0)-coalesce(o.ingestion,0) AS ingestion
  FROM old_counts o FULL JOIN new_counts n USING(stripe,queue)
 ), updated AS (UPDATE queue_backlog_totals t SET pending=t.pending+d.pending,ingestion_pending=t.ingestion_pending+d.ingestion
 FROM deltas d WHERE (t.stripe,t.queue)=(d.stripe,d.queue) AND (d.pending<>0 OR d.ingestion<>0) RETURNING t.stripe)

, removed AS (DELETE FROM queue_backlog_documents WHERE ctid=ANY(ARRAY(
  SELECT d.ctid FROM keys k JOIN LATERAL (
   SELECT ctid,organization,queue,document_id FROM queue_backlog_documents
   WHERE (organization,record_id)=(k.organization,k.record_id) OFFSET 0
  ) d ON true WHERE NOT EXISTS(SELECT FROM desired n
   WHERE (n.organization,n.queue,n.document_id)=(d.organization,d.queue,d.document_id)))) RETURNING document_id)
, inserted AS (INSERT INTO queue_backlog_documents SELECT * FROM desired
 ON CONFLICT(organization,queue,document_id) DO UPDATE SET
  record_id=EXCLUDED.record_id,admitted_at=EXCLUDED.admitted_at,ingestion=EXCLUDED.ingestion,
  ready_at=EXCLUDED.ready_at,ready=EXCLUDED.ready
 WHERE (queue_backlog_documents.record_id,queue_backlog_documents.admitted_at,queue_backlog_documents.ingestion,queue_backlog_documents.ready_at,queue_backlog_documents.ready)
 IS DISTINCT FROM (EXCLUDED.record_id,EXCLUDED.admitted_at,EXCLUDED.ingestion,EXCLUDED.ready_at,EXCLUDED.ready) RETURNING document_id) SELECT 1`,
}
