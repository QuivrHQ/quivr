alter table "public"."notion_sync" add column "sync_user_id" bigint;

alter table "public"."syncs_user" add column "status" text;

alter table "public"."notion_sync" add constraint "public_notion_sync_syncs_user_id_fkey" FOREIGN KEY (sync_user_id) REFERENCES syncs_user(id) ON DELETE CASCADE not valid;

alter table "public"."notion_sync" validate constraint "public_notion_sync_syncs_user_id_fkey";

alter publication supabase_realtime add table "public"."syncs_user"
