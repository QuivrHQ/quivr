CREATE UNIQUE INDEX notion_sync_notion_id_key ON public.notion_sync USING btree (notion_id);

alter table "public"."notion_sync" add constraint "notion_sync_notion_id_key" UNIQUE using index "notion_sync_notion_id_key";
