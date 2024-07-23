drop policy "NOTIFICATIONS" on "public"."onboardings";

revoke delete on table "public"."onboardings" from "anon";

revoke insert on table "public"."onboardings" from "anon";

revoke references on table "public"."onboardings" from "anon";

revoke select on table "public"."onboardings" from "anon";

revoke trigger on table "public"."onboardings" from "anon";

revoke truncate on table "public"."onboardings" from "anon";

revoke update on table "public"."onboardings" from "anon";

revoke delete on table "public"."onboardings" from "authenticated";

revoke insert on table "public"."onboardings" from "authenticated";

revoke references on table "public"."onboardings" from "authenticated";

revoke select on table "public"."onboardings" from "authenticated";

revoke trigger on table "public"."onboardings" from "authenticated";

revoke truncate on table "public"."onboardings" from "authenticated";

revoke update on table "public"."onboardings" from "authenticated";

revoke delete on table "public"."onboardings" from "service_role";

revoke insert on table "public"."onboardings" from "service_role";

revoke references on table "public"."onboardings" from "service_role";

revoke select on table "public"."onboardings" from "service_role";

revoke trigger on table "public"."onboardings" from "service_role";

revoke truncate on table "public"."onboardings" from "service_role";

revoke update on table "public"."onboardings" from "service_role";

alter table "public"."onboardings" drop constraint "onboardings_user_id_fkey";

alter table "public"."onboardings" drop constraint "onboardings_pkey";

drop index if exists "public"."onboardings_pkey";

drop table "public"."onboardings" CASCADE;

drop function if exists public.create_user_onboarding cascade;