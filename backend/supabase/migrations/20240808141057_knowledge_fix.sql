alter table "public"."knowledge" drop column "file_sha";

alter table "public"."knowledge" add column "file_sha1" text;


CREATE INDEX knowledge_file_sha1_hash_idx ON knowledge USING hash (file_sha1);

alter table "public"."knowledge" drop column "brain_id";
