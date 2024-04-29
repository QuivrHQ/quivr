alter table "public"."brain_subscription_invitations" drop constraint "brain_subscription_invitations_brain_id_fkey";

alter table "public"."brains_users" drop constraint "brains_users_brain_id_fkey";

alter table "public"."brains_vectors" drop constraint "brains_vectors_brain_id_fkey";

alter table "public"."chat_history" drop constraint "chat_history_brain_id_fkey";

alter table "public"."knowledge" drop constraint "knowledge_brain_id_fkey";

alter table "public"."knowledge" drop constraint "knowledge_pkey";

drop index if exists "public"."knowledge_pkey";

alter table "public"."integrations_user" add column "last_synced" timestamp with time zone default now();

alter table "public"."brain_subscription_invitations" add constraint "brain_subscription_invitations_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."brain_subscription_invitations" validate constraint "brain_subscription_invitations_brain_id_fkey";

alter table "public"."brains_users" add constraint "brains_users_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."brains_users" validate constraint "brains_users_brain_id_fkey";

alter table "public"."brains_vectors" add constraint "brains_vectors_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."brains_vectors" validate constraint "brains_vectors_brain_id_fkey";

alter table "public"."chat_history" add constraint "chat_history_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."chat_history" validate constraint "chat_history_brain_id_fkey";

alter table "public"."knowledge" add constraint "knowledge_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."knowledge" validate constraint "knowledge_brain_id_fkey";

create policy "Enable all for service role"
on "public"."integrations_user"
as permissive
for all
to service_role
with check (true);



