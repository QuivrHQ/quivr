-- Compatibility bridge: previous binaries keep their synchronous journal.
-- Activation is a later explicit deployment-wide cutover after their retirement.
CREATE SEQUENCE change_event_positions AS bigint CACHE 1;
ALTER TABLE change_events ADD COLUMN writer_xid xid8;

CREATE TABLE change_journal_publication (
 singleton boolean PRIMARY KEY DEFAULT true CHECK(singleton),
 parallel boolean NOT NULL DEFAULT false,
 epoch bigint NOT NULL DEFAULT 0,
 published_through bigint NOT NULL DEFAULT 0,
 sampled_through bigint NOT NULL DEFAULT 0,
 sample_xid xid8,
 sampled_at timestamptz,
 published_at timestamptz
);

CREATE TABLE journal_request_claims (
 organization text NOT NULL,
 family text NOT NULL,
 request_key text NOT NULL,
 PRIMARY KEY(organization,family,request_key)
);

CREATE TABLE change_feed_starts (
 id text PRIMARY KEY,
 organization text NOT NULL,
 corpus_id text NOT NULL,
 snapshot pg_snapshot NOT NULL,
 position bigint NOT NULL,
 ceiling bigint NOT NULL,
 expires_at timestamptz NOT NULL
);

CREATE INDEX change_feed_starts_expiry ON change_feed_starts(organization,expires_at,id);

CREATE TABLE parallel_queue_observations (
 organization text NOT NULL,
 record_id text NOT NULL,
 revision bigint NOT NULL DEFAULT 1,
 applied_revision bigint NOT NULL DEFAULT 0,
 changed_at timestamptz NOT NULL,
 dirty_since timestamptz NOT NULL DEFAULT '-infinity',
 PRIMARY KEY(organization,record_id)
);
CREATE INDEX parallel_queue_observations_dirty ON parallel_queue_observations(organization,record_id)
 WHERE revision<>applied_revision;
