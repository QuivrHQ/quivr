alter table "public"."tasks" add column "assistant_name" text;

alter
  publication supabase_realtime add table tasks;





