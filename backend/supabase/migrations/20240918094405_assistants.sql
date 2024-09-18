alter table "public"."tasks" drop column "answer_pretty";

alter table "public"."tasks" drop column "answer_raw";

alter table "public"."tasks" add column "answer" text;

alter table "public"."tasks" add column "assistant_id" bigint not null;

alter table "public"."tasks" add column "settings" jsonb;


