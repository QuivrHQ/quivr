create table "public"."ingestions" (
    "name" text,
    "id" uuid not null default gen_random_uuid()
);


alter table "public"."ingestions" enable row level security;

CREATE UNIQUE INDEX ingestions_pkey ON public.ingestions USING btree (id);

alter table "public"."ingestions" add constraint "ingestions_pkey" PRIMARY KEY using index "ingestions_pkey";

grant delete on table "public"."ingestions" to "anon";

grant insert on table "public"."ingestions" to "anon";

grant references on table "public"."ingestions" to "anon";

grant select on table "public"."ingestions" to "anon";

grant trigger on table "public"."ingestions" to "anon";

grant truncate on table "public"."ingestions" to "anon";

grant update on table "public"."ingestions" to "anon";

grant delete on table "public"."ingestions" to "authenticated";

grant insert on table "public"."ingestions" to "authenticated";

grant references on table "public"."ingestions" to "authenticated";

grant select on table "public"."ingestions" to "authenticated";

grant trigger on table "public"."ingestions" to "authenticated";

grant truncate on table "public"."ingestions" to "authenticated";

grant update on table "public"."ingestions" to "authenticated";

grant delete on table "public"."ingestions" to "service_role";

grant insert on table "public"."ingestions" to "service_role";

grant references on table "public"."ingestions" to "service_role";

grant select on table "public"."ingestions" to "service_role";

grant trigger on table "public"."ingestions" to "service_role";

grant truncate on table "public"."ingestions" to "service_role";

grant update on table "public"."ingestions" to "service_role";

create policy "INGESTION"
on "public"."ingestions"
as permissive
for all
to service_role;


create policy "INTEGRATIONS"
on "public"."integrations"
as permissive
for all
to service_role;



