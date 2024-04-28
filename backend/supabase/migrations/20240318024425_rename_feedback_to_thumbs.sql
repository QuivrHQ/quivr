alter table "public"."chat_history" drop column "user_feedback";

alter table "public"."chat_history" add column "thumbs" boolean;
