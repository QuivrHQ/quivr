alter table "public"."user_identity" drop column "role_in_company";

alter table "public"."user_identity" add column "usage_purpose" text;
