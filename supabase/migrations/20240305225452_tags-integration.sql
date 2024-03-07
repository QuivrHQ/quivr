create type "public"."brain_tags" as enum ('new', 'recommended', 'most_popular', 'premium', 'coming_soon', 'community', 'deprecated');

alter table "public"."integrations" add column "information" text;

alter table "public"."integrations" add column "tags" brain_tags[];


