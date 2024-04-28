alter table "public"."api_brain_definition" add column "jq_instructions" text not null default ''::text;

alter table "public"."api_brain_definition" add column "raw" boolean not null default false;

alter table "public"."api_brain_definition" alter column "brain_id" set not null;

CREATE UNIQUE INDEX api_brain_definition_pkey ON public.api_brain_definition USING btree (brain_id);

alter table "public"."api_brain_definition" add constraint "api_brain_definition_pkey" PRIMARY KEY using index "api_brain_definition_pkey";


