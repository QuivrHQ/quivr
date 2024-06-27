alter table "public"."integrations" alter column "integration_type" drop default;

alter type "public"."integration_type" rename to "integration_type__old_version_to_be_dropped";

create type "public"."integration_type" as enum ('custom', 'sync', 'doc');

alter table "public"."integrations" alter column integration_type type "public"."integration_type" using integration_type::text::"public"."integration_type";

alter table "public"."integrations" alter column "integration_type" set default 'custom'::integration_type;

drop type "public"."integration_type__old_version_to_be_dropped";
