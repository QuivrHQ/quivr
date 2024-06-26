create type "public"."integration_type" as enum ('custom', 'sync');

alter table "public"."integrations" add column "description" text not null default 'Default description'::text;

alter table "public"."integrations" add column "integration_type" integration_type not null default 'custom'::integration_type;

alter table "public"."integrations" add column "max_files" integer not null default 0;
