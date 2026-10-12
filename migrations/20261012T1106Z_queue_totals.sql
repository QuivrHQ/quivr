-- Queue membership, not corpus/document catalog totals. Finished work has no
-- membership. Fixed counter stripes keep publication independent of backlog size.
CREATE TABLE queue_backlog_documents (
 organization text NOT NULL,
 record_id text NOT NULL,
 queue text NOT NULL CHECK(queue IN ('live','bulk')),
 document_id text NOT NULL,
 admitted_at timestamptz NOT NULL,
 ingestion boolean NOT NULL,
 ready_at timestamptz NOT NULL,
 ready boolean NOT NULL,
 PRIMARY KEY(organization,queue,document_id)
);
CREATE INDEX queue_documents_by_record ON queue_backlog_documents(organization,record_id);
CREATE INDEX queue_documents_arrival ON queue_backlog_documents(queue,admitted_at,organization,document_id) WHERE ready;
CREATE INDEX queue_backlog_due ON queue_backlog_documents(ready_at,organization,record_id) WHERE NOT ready;
CREATE TABLE queue_backlog_totals (
 stripe integer NOT NULL,
 queue text NOT NULL,
 pending bigint NOT NULL DEFAULT 0 CHECK(pending>=0),
 ingestion_pending bigint NOT NULL DEFAULT 0 CHECK(ingestion_pending>=0),
 PRIMARY KEY(stripe,queue)
);
CREATE TABLE queue_backlog_bootstrap (
 singleton boolean PRIMARY KEY DEFAULT true CHECK(singleton),
 organization text NOT NULL DEFAULT '',
 record_id text NOT NULL DEFAULT '',
 initialized boolean NOT NULL DEFAULT false,
 next_run timestamptz NOT NULL DEFAULT '-infinity'
);
CREATE TABLE queue_operation_scope_progress (
 organization text NOT NULL,
 operation_id text NOT NULL,
 cursor text NOT NULL DEFAULT '',
 seen bigint NOT NULL DEFAULT 0,
 PRIMARY KEY(organization,operation_id)
);

-- These gauges count work items, unlike the deduplicated document queues.
CREATE TABLE queue_metric_items (
 source text NOT NULL,
 organization text NOT NULL,
 record_id text NOT NULL DEFAULT '',
 work_id text NOT NULL,
 sequence bigint NOT NULL DEFAULT 0,
 admitted_at timestamptz NOT NULL,
 erroring boolean NOT NULL DEFAULT false,
 PRIMARY KEY(source,organization,work_id,sequence)
);
CREATE INDEX queue_metric_records ON queue_metric_items(source,organization,record_id);
CREATE INDEX queue_metric_arrival ON queue_metric_items(source,admitted_at);
CREATE TABLE queue_metric_totals (
 source text NOT NULL,
 stripe integer NOT NULL,
 pending bigint NOT NULL DEFAULT 0 CHECK(pending>=0),
 erroring bigint NOT NULL DEFAULT 0 CHECK(erroring>=0),
 PRIMARY KEY(source,stripe)
);
CREATE TABLE queue_metric_bootstrap (
 source text PRIMARY KEY,
 organization text NOT NULL DEFAULT '',
 work_id text NOT NULL DEFAULT '',
 sequence bigint NOT NULL DEFAULT 0,
 initialized boolean NOT NULL DEFAULT false,
 next_run timestamptz NOT NULL DEFAULT '-infinity'
);

-- Scope-wide transitions schedule bounded repair rather than materializing
-- their entire scope in a journal transaction.
CREATE TABLE queue_scope_reconciliation (
 kind text NOT NULL CHECK(kind IN ('quarantine','delivery')),
 organization text NOT NULL,
 resource_id text NOT NULL,
 cursor text NOT NULL DEFAULT '',
 PRIMARY KEY(kind,organization,resource_id)
);
