alter table "public"."user_settings" add column "is_premium" boolean not null default false;

alter table "public"."user_settings" alter column "max_brain_size" set not null;

alter table "public"."user_settings" alter column "max_brain_size" set data type bigint using "max_brain_size"::bigint;
