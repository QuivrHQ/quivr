-- Renamed syncs
ALTER TABLE syncs_user
    RENAME TO syncs;
-- Add column foreign key sync in knowledge
ALTER TABLE "public"."knowledge"
ADD COLUMN "sync_id" INTEGER;
ALTER TABLE "public"."knowledge"
ADD CONSTRAINT "public_knowledge_sync_id_fkey" FOREIGN KEY (sync_id) REFERENCES syncs(id) ON DELETE CASCADE;
-- Add column for sync_file_ids
ALTER TABLE "public"."knowledge"
ADD COLUMN "last_synced_at" timestamp with time zone;
ALTER TABLE "public"."knowledge"
ADD COLUMN "sync_file_id" TEXT;
CREATE INDEX knowledge_sync_id_pkey ON public.knowledge USING btree (sync_id);
CREATE INDEX knowledge_sync_file_id_pkey ON public.knowledge USING btree (sync_file_id);
-- Add columns syncs
alter table "public"."syncs"
add column "created_at" timestamp with time zone default now();
alter table "public"."syncs"
add column "updated_at" timestamp with time zone default now();
-- Drop files
DROP TABLE IF EXISTS "public"."syncs_active" CASCADE;
DROP TABLE IF EXISTS "public"."syncs_files" CASCADE;
