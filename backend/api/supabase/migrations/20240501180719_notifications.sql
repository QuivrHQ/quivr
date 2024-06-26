create type "public"."status" as enum ('info', 'warning', 'success', 'error');

alter table "public"."notifications" drop column "action";

alter table "public"."notifications" drop column "chat_id";

alter table "public"."notifications" drop column "message";

alter table "public"."notifications" add column "archived" boolean not null default false;

alter table "public"."notifications" add column "description" text;

alter table "public"."notifications" add column "read" boolean not null default false;

alter table "public"."notifications" add column "title" text not null;

alter table "public"."notifications" add column "user_id" uuid not null;

alter table "public"."notifications" alter column "status" set default 'info'::status;

alter table "public"."notifications" alter column "status" set data type status using "status"::status;

alter table "public"."notifications" add constraint "public_notifications_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."notifications" validate constraint "public_notifications_user_id_fkey";

create policy "allow_user_all_notifications"
on "public"."notifications"
as permissive
for all
to public
using ((user_id = auth.uid()));
