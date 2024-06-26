alter table "public"."product_to_features" drop column "daily_chat_credit";

alter table "public"."product_to_features" add column "monthly_chat_credit" integer not null default 20;

alter table "public"."user_settings" drop column "daily_chat_credit";

alter table "public"."user_settings" add column "monthly_chat_credit" integer default 100;
