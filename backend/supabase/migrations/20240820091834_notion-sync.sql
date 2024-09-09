create table "public"."notion_sync" (
    "id" UUID DEFAULT uuid_generate_v4() not null,
    "notion_id" uuid not null,
    "parent_id" uuid,
    "is_folder" boolean,
    "icon" text,
    "last_modified" timestamp with time zone,
    "web_view_link" text,
    "type" text,
    "name" text,
    "mime_type" text,
    "user_id" text
);
alter table "public"."notion_sync" enable row level security;
alter table "public"."syncs_active"
add column if not exists "notification_id" uuid;

CREATE UNIQUE INDEX notion_sync_pkey ON public.notion_sync USING btree (id, notion_id);

alter table "public"."notion_sync"
add constraint "notion_sync_pkey" PRIMARY KEY using index "notion_sync_pkey";
grant delete on table "public"."notion_sync" to "anon";
grant insert on table "public"."notion_sync" to "anon";
grant references on table "public"."notion_sync" to "anon";
grant select on table "public"."notion_sync" to "anon";
grant trigger on table "public"."notion_sync" to "anon";
grant truncate on table "public"."notion_sync" to "anon";
grant update on table "public"."notion_sync" to "anon";
grant delete on table "public"."notion_sync" to "authenticated";
grant insert on table "public"."notion_sync" to "authenticated";
grant references on table "public"."notion_sync" to "authenticated";
grant select on table "public"."notion_sync" to "authenticated";
grant trigger on table "public"."notion_sync" to "authenticated";
grant truncate on table "public"."notion_sync" to "authenticated";
grant update on table "public"."notion_sync" to "authenticated";
grant delete on table "public"."notion_sync" to "service_role";
grant insert on table "public"."notion_sync" to "service_role";
grant references on table "public"."notion_sync" to "service_role";
grant select on table "public"."notion_sync" to "service_role";
grant trigger on table "public"."notion_sync" to "service_role";
grant truncate on table "public"."notion_sync" to "service_role";
grant update on table "public"."notion_sync" to "service_role";

CREATE UNIQUE INDEX notion_sync_notion_id_key ON public.notion_sync USING btree (notion_id);

alter table "public"."notion_sync" add constraint "notion_sync_notion_id_key" UNIQUE using index "notion_sync_notion_id_key";
