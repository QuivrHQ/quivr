drop policy "INGESTION" on "public"."ingestions";

revoke delete on table "public"."ingestions" from "anon";

revoke insert on table "public"."ingestions" from "anon";

revoke references on table "public"."ingestions" from "anon";

revoke select on table "public"."ingestions" from "anon";

revoke trigger on table "public"."ingestions" from "anon";

revoke truncate on table "public"."ingestions" from "anon";

revoke update on table "public"."ingestions" from "anon";

revoke delete on table "public"."ingestions" from "authenticated";

revoke insert on table "public"."ingestions" from "authenticated";

revoke references on table "public"."ingestions" from "authenticated";

revoke select on table "public"."ingestions" from "authenticated";

revoke trigger on table "public"."ingestions" from "authenticated";

revoke truncate on table "public"."ingestions" from "authenticated";

revoke update on table "public"."ingestions" from "authenticated";

revoke delete on table "public"."ingestions" from "service_role";

revoke insert on table "public"."ingestions" from "service_role";

revoke references on table "public"."ingestions" from "service_role";

revoke select on table "public"."ingestions" from "service_role";

revoke trigger on table "public"."ingestions" from "service_role";

revoke truncate on table "public"."ingestions" from "service_role";

revoke update on table "public"."ingestions" from "service_role";

alter table "public"."ingestions" drop constraint "ingestions_pkey";

drop index if exists "public"."ingestions_pkey";

drop table "public"."ingestions";

create table "public"."assistants" (
    "name" text,
    "id" uuid not null default gen_random_uuid(),
    "brain_id_required" boolean not null default true,
    "file_1_required" boolean not null default false,
    "url_required" boolean default false
);


alter table "public"."assistants" enable row level security;

CREATE UNIQUE INDEX ingestions_pkey ON public.assistants USING btree (id);

alter table "public"."assistants" add constraint "ingestions_pkey" PRIMARY KEY using index "ingestions_pkey";

grant delete on table "public"."assistants" to "anon";

grant insert on table "public"."assistants" to "anon";

grant references on table "public"."assistants" to "anon";

grant select on table "public"."assistants" to "anon";

grant trigger on table "public"."assistants" to "anon";

grant truncate on table "public"."assistants" to "anon";

grant update on table "public"."assistants" to "anon";

grant delete on table "public"."assistants" to "authenticated";

grant insert on table "public"."assistants" to "authenticated";

grant references on table "public"."assistants" to "authenticated";

grant select on table "public"."assistants" to "authenticated";

grant trigger on table "public"."assistants" to "authenticated";

grant truncate on table "public"."assistants" to "authenticated";

grant update on table "public"."assistants" to "authenticated";

grant delete on table "public"."assistants" to "service_role";

grant insert on table "public"."assistants" to "service_role";

grant references on table "public"."assistants" to "service_role";

grant select on table "public"."assistants" to "service_role";

grant trigger on table "public"."assistants" to "service_role";

grant truncate on table "public"."assistants" to "service_role";

grant update on table "public"."assistants" to "service_role";

create policy "INGESTION"
on "public"."assistants"
as permissive
for all
to service_role;



