ALTER TABLE "public"."knowledge"
    RENAME COLUMN "integration" TO "source";
ALTER TABLE "public"."knowledge"
    RENAME COLUMN "integration_link" TO "source_link";
ALTER TABLE "public"."knowledge"
add column "file_sha1" text;
ALTER TABLE "public"."knowledge"
add CONSTRAINT "unique_file_sha1" unique ("file_sha1");
alter table "public"."knowledge"
add column "created_at" timestamp with time zone default now();
alter table "public"."knowledge"
add column "file_size" bigint;
alter table "public"."knowledge"
add column "metadata" jsonb;
alter table "public"."knowledge"
add column "updated_at" timestamp with time zone default now();
CREATE INDEX knowledge_file_sha1_hash_idx ON knowledge USING hash (file_sha1);
