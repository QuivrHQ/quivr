-- Private completion state is initialized lazily for existing running rebuilds.
CREATE TABLE projection_rebuild_validation (
 organization text NOT NULL, operation_id text NOT NULL, corpus_id text NOT NULL,
 fingerprint jsonb NOT NULL, scan_cursor text NOT NULL DEFAULT '',
 scanned boolean NOT NULL DEFAULT false, owner_gap boolean NOT NULL DEFAULT false,
 PRIMARY KEY(organization,operation_id)
);
CREATE INDEX projection_rebuild_validation_pending ON projection_rebuild_validation(organization,corpus_id,operation_id);
CREATE TABLE projection_rebuild_dirty_records (
 organization text NOT NULL, operation_id text NOT NULL, record_id text NOT NULL,
 version_id text NOT NULL DEFAULT '', revision bigint NOT NULL DEFAULT 1,
 checked boolean NOT NULL DEFAULT false, owner_gap boolean NOT NULL DEFAULT false,
 PRIMARY KEY(organization,operation_id,record_id)
);
CREATE INDEX projection_rebuild_dirty_versions ON projection_rebuild_dirty_records(organization,operation_id,version_id);
CREATE INDEX projection_rebuild_dirty_pending ON projection_rebuild_dirty_records(organization,operation_id,record_id) WHERE NOT checked;
CREATE INDEX projection_rebuild_dirty_owners ON projection_rebuild_dirty_records(organization,operation_id,record_id) WHERE checked AND owner_gap;
