alter table "public"."knowledge" drop column "extension";

alter table "public"."knowledge" drop column "integration";

alter table "public"."knowledge" drop column "integration_link";

alter table "public"."knowledge" add column "created_at" timestamp with time zone default now();

alter table "public"."knowledge" add column "file_sha" text;

alter table "public"."knowledge" add column "file_size" bigint;

alter table "public"."knowledge" add column "metadata" jsonb;

alter table "public"."knowledge" add column "mime_type" text not null;

alter table "public"."knowledge" add column "source" text default 'Local'::text;

alter table "public"."knowledge" add column "source_link" text;

alter table "public"."knowledge" add column "updated_at" timestamp with time zone default now();

CREATE UNIQUE INDEX notion_sync_notion_id_key ON public.notion_sync USING btree (notion_id);

alter table "public"."notion_sync" add constraint "notion_sync_notion_id_key" UNIQUE using index "notion_sync_notion_id_key";


