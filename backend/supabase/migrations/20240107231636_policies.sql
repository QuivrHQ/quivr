revoke delete on table "public"."knowledge_vectors" from "anon";

revoke insert on table "public"."knowledge_vectors" from "anon";

revoke references on table "public"."knowledge_vectors" from "anon";

revoke select on table "public"."knowledge_vectors" from "anon";

revoke trigger on table "public"."knowledge_vectors" from "anon";

revoke truncate on table "public"."knowledge_vectors" from "anon";

revoke update on table "public"."knowledge_vectors" from "anon";

revoke delete on table "public"."knowledge_vectors" from "authenticated";

revoke insert on table "public"."knowledge_vectors" from "authenticated";

revoke references on table "public"."knowledge_vectors" from "authenticated";

revoke select on table "public"."knowledge_vectors" from "authenticated";

revoke trigger on table "public"."knowledge_vectors" from "authenticated";

revoke truncate on table "public"."knowledge_vectors" from "authenticated";

revoke update on table "public"."knowledge_vectors" from "authenticated";

revoke delete on table "public"."knowledge_vectors" from "service_role";

revoke insert on table "public"."knowledge_vectors" from "service_role";

revoke references on table "public"."knowledge_vectors" from "service_role";

revoke select on table "public"."knowledge_vectors" from "service_role";

revoke trigger on table "public"."knowledge_vectors" from "service_role";

revoke truncate on table "public"."knowledge_vectors" from "service_role";

revoke update on table "public"."knowledge_vectors" from "service_role";

revoke delete on table "public"."stats" from "anon";

revoke insert on table "public"."stats" from "anon";

revoke references on table "public"."stats" from "anon";

revoke select on table "public"."stats" from "anon";

revoke trigger on table "public"."stats" from "anon";

revoke truncate on table "public"."stats" from "anon";

revoke update on table "public"."stats" from "anon";

revoke delete on table "public"."stats" from "authenticated";

revoke insert on table "public"."stats" from "authenticated";

revoke references on table "public"."stats" from "authenticated";

revoke select on table "public"."stats" from "authenticated";

revoke trigger on table "public"."stats" from "authenticated";

revoke truncate on table "public"."stats" from "authenticated";

revoke update on table "public"."stats" from "authenticated";

revoke delete on table "public"."stats" from "service_role";

revoke insert on table "public"."stats" from "service_role";

revoke references on table "public"."stats" from "service_role";

revoke select on table "public"."stats" from "service_role";

revoke trigger on table "public"."stats" from "service_role";

revoke truncate on table "public"."stats" from "service_role";

revoke update on table "public"."stats" from "service_role";

revoke delete on table "public"."summaries" from "anon";

revoke insert on table "public"."summaries" from "anon";

revoke references on table "public"."summaries" from "anon";

revoke select on table "public"."summaries" from "anon";

revoke trigger on table "public"."summaries" from "anon";

revoke truncate on table "public"."summaries" from "anon";

revoke update on table "public"."summaries" from "anon";

revoke delete on table "public"."summaries" from "authenticated";

revoke insert on table "public"."summaries" from "authenticated";

revoke references on table "public"."summaries" from "authenticated";

revoke select on table "public"."summaries" from "authenticated";

revoke trigger on table "public"."summaries" from "authenticated";

revoke truncate on table "public"."summaries" from "authenticated";

revoke update on table "public"."summaries" from "authenticated";

revoke delete on table "public"."summaries" from "service_role";

revoke insert on table "public"."summaries" from "service_role";

revoke references on table "public"."summaries" from "service_role";

revoke select on table "public"."summaries" from "service_role";

revoke trigger on table "public"."summaries" from "service_role";

revoke truncate on table "public"."summaries" from "service_role";

revoke update on table "public"."summaries" from "service_role";

revoke delete on table "public"."users_old" from "anon";

revoke insert on table "public"."users_old" from "anon";

revoke references on table "public"."users_old" from "anon";

revoke select on table "public"."users_old" from "anon";

revoke trigger on table "public"."users_old" from "anon";

revoke truncate on table "public"."users_old" from "anon";

revoke update on table "public"."users_old" from "anon";

revoke delete on table "public"."users_old" from "authenticated";

revoke insert on table "public"."users_old" from "authenticated";

revoke references on table "public"."users_old" from "authenticated";

revoke select on table "public"."users_old" from "authenticated";

revoke trigger on table "public"."users_old" from "authenticated";

revoke truncate on table "public"."users_old" from "authenticated";

revoke update on table "public"."users_old" from "authenticated";

revoke delete on table "public"."users_old" from "service_role";

revoke insert on table "public"."users_old" from "service_role";

revoke references on table "public"."users_old" from "service_role";

revoke select on table "public"."users_old" from "service_role";

revoke trigger on table "public"."users_old" from "service_role";

revoke truncate on table "public"."users_old" from "service_role";

revoke update on table "public"."users_old" from "service_role";

revoke delete on table "public"."vectors_old" from "anon";

revoke insert on table "public"."vectors_old" from "anon";

revoke references on table "public"."vectors_old" from "anon";

revoke select on table "public"."vectors_old" from "anon";

revoke trigger on table "public"."vectors_old" from "anon";

revoke truncate on table "public"."vectors_old" from "anon";

revoke update on table "public"."vectors_old" from "anon";

revoke delete on table "public"."vectors_old" from "authenticated";

revoke insert on table "public"."vectors_old" from "authenticated";

revoke references on table "public"."vectors_old" from "authenticated";

revoke select on table "public"."vectors_old" from "authenticated";

revoke trigger on table "public"."vectors_old" from "authenticated";

revoke truncate on table "public"."vectors_old" from "authenticated";

revoke update on table "public"."vectors_old" from "authenticated";

revoke delete on table "public"."vectors_old" from "service_role";

revoke insert on table "public"."vectors_old" from "service_role";

revoke references on table "public"."vectors_old" from "service_role";

revoke select on table "public"."vectors_old" from "service_role";

revoke trigger on table "public"."vectors_old" from "service_role";

revoke truncate on table "public"."vectors_old" from "service_role";

revoke update on table "public"."vectors_old" from "service_role";

alter table "public"."knowledge_vectors" drop constraint "knowledge_vectors_knowledge_id_fkey";

alter table "public"."notifications" drop constraint "notifications_chat_id_fkey";

alter table "public"."api_keys" drop constraint "api_keys_user_id_fkey";

alter table "public"."brains_users" drop constraint "brains_users_brain_id_fkey";

alter table "public"."brains_users" drop constraint "brains_users_user_id_fkey";

alter table "public"."chat_history" drop constraint "chat_history_chat_id_fkey";

alter table "public"."chats" drop constraint "chats_user_id_fkey";

alter table "public"."onboardings" drop constraint "onboardings_user_id_fkey";

alter table "public"."user_daily_usage" drop constraint "user_daily_usage_user_id_fkey";

alter table "public"."users" drop constraint "users_id_fkey";

alter table "public"."knowledge_vectors" drop constraint "knowledge_vectors_pkey";

alter table "public"."stats" drop constraint "stats_pkey";

alter table "public"."summaries" drop constraint "summaries_pkey";

alter table "public"."vectors_old" drop constraint "vectors_pkey";

drop table if exists "public"."documents";

drop table "public"."knowledge_vectors";

drop table if exists "public"."migrations";

drop table "public"."stats";

drop table "public"."summaries";

drop table "public"."users_old";

drop table "public"."vectors_old";

drop index if exists "public"."knowledge_vectors_pkey";

drop index if exists "public"."migrations_pkey";

drop index if exists "public"."stats_pkey";

drop index if exists "public"."summaries_pkey";

drop index if exists "public"."vectors_pkey";

alter table "public"."api_brain_definition" enable row level security;

alter table "public"."api_keys" enable row level security;

alter table "public"."brain_subscription_invitations" enable row level security;

alter table "public"."brains" enable row level security;

alter table "public"."brains_users" enable row level security;

alter table "public"."brains_vectors" enable row level security;

alter table "public"."chat_history" enable row level security;

alter table "public"."chats" enable row level security;

alter table "public"."composite_brain_connections" enable row level security;

alter table "public"."knowledge" enable row level security;

alter table "public"."models" enable row level security;

alter table "public"."notifications" enable row level security;

alter table "public"."onboardings" enable row level security;

alter table "public"."product_to_features" enable row level security;

alter table "public"."prompts" enable row level security;

alter table "public"."user_daily_usage" enable row level security;

alter table "public"."user_identity" enable row level security;

alter table "public"."user_settings" enable row level security;

alter table "public"."users" enable row level security;

alter table "public"."vectors" enable row level security;

drop sequence if exists "public"."documents_id_seq";

drop sequence if exists "public"."summaries_id_seq";

drop sequence if exists "public"."vectors_id_seq";

alter table "public"."user_identity" add constraint "user_identity_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."user_identity" validate constraint "user_identity_user_id_fkey";

alter table "public"."user_settings" add constraint "user_settings_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."user_settings" validate constraint "user_settings_user_id_fkey";

alter table "public"."api_keys" add constraint "api_keys_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."api_keys" validate constraint "api_keys_user_id_fkey";

alter table "public"."brains_users" add constraint "brains_users_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) ON DELETE CASCADE not valid;

alter table "public"."brains_users" validate constraint "brains_users_brain_id_fkey";

alter table "public"."brains_users" add constraint "brains_users_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."brains_users" validate constraint "brains_users_user_id_fkey";

alter table "public"."chat_history" add constraint "chat_history_chat_id_fkey" FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE not valid;

alter table "public"."chat_history" validate constraint "chat_history_chat_id_fkey";

alter table "public"."chats" add constraint "chats_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."chats" validate constraint "chats_user_id_fkey";

alter table "public"."onboardings" add constraint "onboardings_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."onboardings" validate constraint "onboardings_user_id_fkey";

alter table "public"."user_daily_usage" add constraint "user_daily_usage_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."user_daily_usage" validate constraint "user_daily_usage_user_id_fkey";

alter table "public"."users" add constraint "users_id_fkey" FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."users" validate constraint "users_id_fkey";

create policy "API_BRAIN_DEFINITION"
on "public"."api_brain_definition"
as permissive
for all
to service_role;


create policy "API_KEYS"
on "public"."api_keys"
as permissive
for all
to service_role;


create policy "BRAIN_SUBSCRIPTION_INVITATIONS"
on "public"."brain_subscription_invitations"
as permissive
for all
to service_role;


create policy "BRAINS"
on "public"."brains"
as permissive
for all
to service_role;


create policy "BRAINS_USERS"
on "public"."brains_users"
as permissive
for all
to service_role;


create policy "BRAINS_VECTORS"
on "public"."brains_vectors"
as permissive
for all
to service_role;


create policy "CHAT_HISTORY"
on "public"."chat_history"
as permissive
for all
to service_role;


create policy "CHATS"
on "public"."chats"
as permissive
for all
to service_role;


create policy "COMPOSITE_BRAIN_CONNECTIONS"
on "public"."composite_brain_connections"
as permissive
for all
to service_role;


create policy "KNOWLEDGE"
on "public"."knowledge"
as permissive
for all
to service_role;


create policy "MODELS"
on "public"."models"
as permissive
for all
to service_role;


create policy "NOTIFICATIONS"
on "public"."notifications"
as permissive
for all
to service_role;


create policy "NOTIFICATIONS"
on "public"."onboardings"
as permissive
for all
to service_role;


create policy "PRODUCT_TO_FEATURES"
on "public"."product_to_features"
as permissive
for all
to service_role;


create policy "PROMPTS"
on "public"."prompts"
as permissive
for all
to service_role;


create policy "USER_DAILY_USAGE"
on "public"."user_daily_usage"
as permissive
for all
to service_role;


create policy "USER_IDENTITY"
on "public"."user_identity"
as permissive
for all
to service_role;


create policy "USER_SETTINGS"
on "public"."user_settings"
as permissive
for all
to service_role;


create policy "USERS"
on "public"."users"
as permissive
for all
to public;


create policy "VECTORS"
on "public"."vectors"
as permissive
for all
to service_role;
