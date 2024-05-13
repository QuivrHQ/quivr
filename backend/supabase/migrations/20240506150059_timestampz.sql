alter table "public"."notifications" alter column "datetime" set default (now() AT TIME ZONE 'utc'::text);

alter table "public"."notifications" alter column "datetime" set data type timestamp with time zone using "datetime"::timestamp with time zone;

alter
  publication supabase_realtime add table notifications


