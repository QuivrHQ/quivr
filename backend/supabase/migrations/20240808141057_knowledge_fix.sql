alter table "public"."knowledge" drop column "file_sha";

alter table "public"."knowledge" drop column "metadata";

alter table "public"."knowledge" add column "file_sha1" text;

alter table "public"."knowledge" add column "metadata_" jsonb;


