alter table "public"."user_identity" drop constraint "user_identity_user_id_fkey";

alter table "public"."user_identity" add column "company" text;

alter table "public"."user_identity" add column "onboarded" boolean not null default false;

alter table "public"."user_identity" add column "username" text;

alter table "public"."users" add column "onboarded" boolean not null default false;

alter table "public"."user_identity" add constraint "public_user_identity_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."user_identity" validate constraint "public_user_identity_user_id_fkey";
