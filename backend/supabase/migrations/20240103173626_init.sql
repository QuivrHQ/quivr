create extension if not exists "vector" with schema "public" ;

create extension if not exists "wrappers" with schema "public";

create type "public"."brain_type_enum" as enum ('doc', 'api', 'composite');

create sequence "public"."summaries_id_seq";

create sequence "public"."vectors_id_seq";

create table "public"."api_brain_definition" (
    "brain_id" uuid,
    "method" character varying(255),
    "url" character varying(255),
    "params" json,
    "search_params" json,
    "secrets" json
);


create table "public"."api_keys" (
    "key_id" uuid not null default gen_random_uuid(),
    "user_id" uuid,
    "api_key" text,
    "creation_time" timestamp without time zone default CURRENT_TIMESTAMP,
    "deleted_time" timestamp without time zone,
    "is_active" boolean default true,
    "name" text default 'API_KEY'::text,
    "days" integer default 30,
    "only_chat" boolean default false
);


create table "public"."brain_subscription_invitations" (
    "brain_id" uuid not null,
    "email" character varying(255) not null,
    "rights" character varying(255)
);


create table "public"."brains" (
    "brain_id" uuid not null default gen_random_uuid(),
    "name" text,
    "status" text,
    "model" text,
    "max_tokens" integer,
    "temperature" double precision,
    "description" text,
    "prompt_id" uuid,
    "retrieval_algorithm" text,
    "last_update" timestamp without time zone default CURRENT_TIMESTAMP,
    "brain_type" brain_type_enum default 'doc'::brain_type_enum
);


create table "public"."brains_users" (
    "brain_id" uuid not null,
    "rights" character varying(255),
    "default_brain" boolean,
    "user_id" uuid
);


create table "public"."brains_vectors" (
    "brain_id" uuid not null,
    "rights" character varying(255),
    "file_sha1" text,
    "vector_id" uuid
);


create table "public"."chat_history" (
    "message_id" uuid not null default uuid_generate_v4(),
    "chat_id" uuid not null,
    "user_message" text,
    "assistant" text,
    "message_time" timestamp without time zone default CURRENT_TIMESTAMP,
    "brain_id" uuid,
    "prompt_id" uuid
);


create table "public"."chats" (
    "chat_id" uuid not null default uuid_generate_v4(),
    "user_id" uuid,
    "creation_time" timestamp without time zone default CURRENT_TIMESTAMP,
    "history" jsonb,
    "chat_name" text
);


create table "public"."composite_brain_connections" (
    "composite_brain_id" uuid not null,
    "connected_brain_id" uuid not null
);


create table "public"."knowledge" (
    "id" uuid not null default gen_random_uuid(),
    "file_name" text,
    "url" text,
    "brain_id" uuid not null,
    "extension" text not null
);


create table "public"."knowledge_vectors" (
    "knowledge_id" uuid not null,
    "vector_id" uuid not null,
    "embedding_model" text not null
);


create table "public"."migrations" (
    "name" character varying(255) not null,
    "executed_at" timestamp with time zone default CURRENT_TIMESTAMP
);


create table "public"."notifications" (
    "id" uuid not null default gen_random_uuid(),
    "datetime" timestamp without time zone default CURRENT_TIMESTAMP,
    "chat_id" uuid,
    "message" text,
    "action" character varying(255) not null,
    "status" character varying(255) not null
);


create table "public"."onboardings" (
    "user_id" uuid not null,
    "onboarding_a" boolean not null default true,
    "onboarding_b1" boolean not null default true,
    "onboarding_b2" boolean not null default true,
    "onboarding_b3" boolean not null default true,
    "creation_time" timestamp without time zone default CURRENT_TIMESTAMP
);


create table "public"."prompts" (
    "id" uuid not null default uuid_generate_v4(),
    "title" character varying(255),
    "content" text,
    "status" character varying(255) default 'private'::character varying
);


create table "public"."stats" (
    "time" timestamp without time zone,
    "chat" boolean,
    "embedding" boolean,
    "details" text,
    "metadata" jsonb,
    "id" integer generated always as identity not null
);


create table "public"."summaries" (
    "id" bigint not null default nextval('summaries_id_seq'::regclass),
    "content" text,
    "metadata" jsonb,
    "embedding" vector(1536),
    "document_id" uuid
);


create table "public"."user_daily_usage" (
    "user_id" uuid not null,
    "email" text,
    "date" text not null,
    "daily_requests_count" integer
);


create table "public"."user_identity" (
    "user_id" uuid not null,
    "openai_api_key" character varying(255)
);


create table "public"."user_settings" (
    "user_id" uuid not null,
    "models" jsonb default '["gpt-3.5-turbo-1106"]'::jsonb,
    "daily_chat_credit" integer default 20,
    "max_brains" integer default 3,
    "max_brain_size" integer default 1000000
);


create table "public"."users" (
    "id" uuid not null,
    "email" text
);


create table "public"."users_old" (
    "user_id" uuid,
    "email" text,
    "date" text,
    "requests_count" integer,
    "supabase_id" uuid
);


create table "public"."vectors" (
    "id" uuid not null default uuid_generate_v4(),
    "content" text,
    "file_sha1" text,
    "metadata" jsonb,
    "embedding" vector(1536)
);


create table "public"."vectors_old" (
    "id" bigint not null default nextval('vectors_id_seq'::regclass),
    "content" text,
    "metadata" jsonb,
    "embedding" vector(1536)
);


alter sequence "public"."summaries_id_seq" owned by "public"."summaries"."id";

alter sequence "public"."vectors_id_seq" owned by "public"."vectors_old"."id";

CREATE UNIQUE INDEX api_keys_api_key_key ON public.api_keys USING btree (api_key);

CREATE UNIQUE INDEX api_keys_pkey ON public.api_keys USING btree (key_id);

CREATE UNIQUE INDEX brain_subscription_invitations_pkey ON public.brain_subscription_invitations USING btree (brain_id, email);

CREATE UNIQUE INDEX brains_pkey ON public.brains USING btree (brain_id);

CREATE UNIQUE INDEX chat_history_pkey ON public.chat_history USING btree (chat_id, message_id);

CREATE UNIQUE INDEX chats_pkey ON public.chats USING btree (chat_id);

CREATE UNIQUE INDEX composite_brain_connections_pkey ON public.composite_brain_connections USING btree (composite_brain_id, connected_brain_id);

CREATE UNIQUE INDEX knowledge_pkey ON public.knowledge USING btree (id);

CREATE UNIQUE INDEX knowledge_vectors_pkey ON public.knowledge_vectors USING btree (knowledge_id, vector_id, embedding_model);

CREATE UNIQUE INDEX migrations_pkey ON public.migrations USING btree (name);

CREATE UNIQUE INDEX notifications_pkey ON public.notifications USING btree (id);

CREATE UNIQUE INDEX onboardings_pkey ON public.onboardings USING btree (user_id);

CREATE UNIQUE INDEX prompts_pkey ON public.prompts USING btree (id);

CREATE UNIQUE INDEX stats_pkey ON public.stats USING btree (id);

CREATE UNIQUE INDEX summaries_pkey ON public.summaries USING btree (id);

CREATE UNIQUE INDEX user_daily_usage_pkey ON public.user_daily_usage USING btree (user_id, date);

CREATE UNIQUE INDEX user_identity_pkey ON public.user_identity USING btree (user_id);

CREATE UNIQUE INDEX user_settings_pkey ON public.user_settings USING btree (user_id);

CREATE UNIQUE INDEX users_pkey ON public.users USING btree (id);

CREATE UNIQUE INDEX vectors_pkey ON public.vectors_old USING btree (id);

CREATE UNIQUE INDEX vectors_pkey1 ON public.vectors USING btree (id);

alter table "public"."api_keys" add constraint "api_keys_pkey" PRIMARY KEY using index "api_keys_pkey";

alter table "public"."brain_subscription_invitations" add constraint "brain_subscription_invitations_pkey" PRIMARY KEY using index "brain_subscription_invitations_pkey";

alter table "public"."brains" add constraint "brains_pkey" PRIMARY KEY using index "brains_pkey";

alter table "public"."chat_history" add constraint "chat_history_pkey" PRIMARY KEY using index "chat_history_pkey";

alter table "public"."chats" add constraint "chats_pkey" PRIMARY KEY using index "chats_pkey";

alter table "public"."composite_brain_connections" add constraint "composite_brain_connections_pkey" PRIMARY KEY using index "composite_brain_connections_pkey";

alter table "public"."knowledge" add constraint "knowledge_pkey" PRIMARY KEY using index "knowledge_pkey";

alter table "public"."knowledge_vectors" add constraint "knowledge_vectors_pkey" PRIMARY KEY using index "knowledge_vectors_pkey";

alter table "public"."migrations" add constraint "migrations_pkey" PRIMARY KEY using index "migrations_pkey";

alter table "public"."notifications" add constraint "notifications_pkey" PRIMARY KEY using index "notifications_pkey";

alter table "public"."onboardings" add constraint "onboardings_pkey" PRIMARY KEY using index "onboardings_pkey";

alter table "public"."prompts" add constraint "prompts_pkey" PRIMARY KEY using index "prompts_pkey";

alter table "public"."stats" add constraint "stats_pkey" PRIMARY KEY using index "stats_pkey";

alter table "public"."summaries" add constraint "summaries_pkey" PRIMARY KEY using index "summaries_pkey";

alter table "public"."user_daily_usage" add constraint "user_daily_usage_pkey" PRIMARY KEY using index "user_daily_usage_pkey";

alter table "public"."user_identity" add constraint "user_identity_pkey" PRIMARY KEY using index "user_identity_pkey";

alter table "public"."user_settings" add constraint "user_settings_pkey" PRIMARY KEY using index "user_settings_pkey";

alter table "public"."users" add constraint "users_pkey" PRIMARY KEY using index "users_pkey";

alter table "public"."vectors" add constraint "vectors_pkey1" PRIMARY KEY using index "vectors_pkey1";

alter table "public"."vectors_old" add constraint "vectors_pkey" PRIMARY KEY using index "vectors_pkey";

alter table "public"."api_brain_definition" add constraint "api_brain_definition_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) not valid;

alter table "public"."api_brain_definition" validate constraint "api_brain_definition_brain_id_fkey";

alter table "public"."api_brain_definition" add constraint "api_brain_definition_method_check" CHECK (((method)::text = ANY ((ARRAY['GET'::character varying, 'POST'::character varying, 'PUT'::character varying, 'DELETE'::character varying])::text[]))) not valid;

alter table "public"."api_brain_definition" validate constraint "api_brain_definition_method_check";

alter table "public"."api_keys" add constraint "api_keys_api_key_key" UNIQUE using index "api_keys_api_key_key";

alter table "public"."brain_subscription_invitations" add constraint "brain_subscription_invitations_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) not valid;

alter table "public"."brain_subscription_invitations" validate constraint "brain_subscription_invitations_brain_id_fkey";

alter table "public"."brains" add constraint "brains_prompt_id_fkey" FOREIGN KEY (prompt_id) REFERENCES prompts(id) not valid;

alter table "public"."brains" validate constraint "brains_prompt_id_fkey";

alter table "public"."brains_users" add constraint "brains_users_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) not valid;

alter table "public"."brains_users" validate constraint "brains_users_brain_id_fkey";

alter table "public"."brains_users" add constraint "brains_users_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) not valid;

alter table "public"."brains_users" validate constraint "brains_users_user_id_fkey";

alter table "public"."brains_vectors" add constraint "brains_vectors_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) not valid;

alter table "public"."brains_vectors" validate constraint "brains_vectors_brain_id_fkey";

alter table "public"."chat_history" add constraint "chat_history_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) not valid;

alter table "public"."chat_history" validate constraint "chat_history_brain_id_fkey";

alter table "public"."chat_history" add constraint "chat_history_chat_id_fkey" FOREIGN KEY (chat_id) REFERENCES chats(chat_id) not valid;

alter table "public"."chat_history" validate constraint "chat_history_chat_id_fkey";

alter table "public"."chat_history" add constraint "chat_history_prompt_id_fkey" FOREIGN KEY (prompt_id) REFERENCES prompts(id) not valid;

alter table "public"."chat_history" validate constraint "chat_history_prompt_id_fkey";

alter table "public"."chats" add constraint "chats_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) not valid;

alter table "public"."chats" validate constraint "chats_user_id_fkey";

alter table "public"."composite_brain_connections" add constraint "composite_brain_connections_check" CHECK ((composite_brain_id <> connected_brain_id)) not valid;

alter table "public"."composite_brain_connections" validate constraint "composite_brain_connections_check";

alter table "public"."composite_brain_connections" add constraint "composite_brain_connections_composite_brain_id_fkey" FOREIGN KEY (composite_brain_id) REFERENCES brains(brain_id) not valid;

alter table "public"."composite_brain_connections" validate constraint "composite_brain_connections_composite_brain_id_fkey";

alter table "public"."composite_brain_connections" add constraint "composite_brain_connections_connected_brain_id_fkey" FOREIGN KEY (connected_brain_id) REFERENCES brains(brain_id) not valid;

alter table "public"."composite_brain_connections" validate constraint "composite_brain_connections_connected_brain_id_fkey";

alter table "public"."knowledge" add constraint "knowledge_brain_id_fkey" FOREIGN KEY (brain_id) REFERENCES brains(brain_id) not valid;

alter table "public"."knowledge" validate constraint "knowledge_brain_id_fkey";

alter table "public"."knowledge" add constraint "knowledge_check" CHECK ((((file_name IS NOT NULL) AND (url IS NULL)) OR ((file_name IS NULL) AND (url IS NOT NULL)))) not valid;

alter table "public"."knowledge" validate constraint "knowledge_check";

alter table "public"."knowledge_vectors" add constraint "knowledge_vectors_knowledge_id_fkey" FOREIGN KEY (knowledge_id) REFERENCES knowledge(id) not valid;

alter table "public"."knowledge_vectors" validate constraint "knowledge_vectors_knowledge_id_fkey";

alter table "public"."notifications" add constraint "notifications_chat_id_fkey" FOREIGN KEY (chat_id) REFERENCES chats(chat_id) not valid;

alter table "public"."notifications" validate constraint "notifications_chat_id_fkey";

alter table "public"."onboardings" add constraint "onboardings_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) not valid;

alter table "public"."onboardings" validate constraint "onboardings_user_id_fkey";

alter table "public"."user_daily_usage" add constraint "user_daily_usage_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) not valid;

alter table "public"."user_daily_usage" validate constraint "user_daily_usage_user_id_fkey";

alter table "public"."users" add constraint "users_id_fkey" FOREIGN KEY (id) REFERENCES auth.users(id) not valid;

alter table "public"."users" validate constraint "users_id_fkey";

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.create_user_onboarding()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
BEGIN
    INSERT INTO public.onboardings (user_id)
    VALUES (NEW.id);
    RETURN NEW;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.delete_secret(secret_name text)
 RETURNS text
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
declare
 deleted_rows int;
begin
 delete from vault.decrypted_secrets where name = secret_name;
 get diagnostics deleted_rows = row_count;
 if deleted_rows = 0 then
   return false;
 else
   return true;
 end if;
end;
$function$
;

CREATE OR REPLACE FUNCTION public.get_premium_user(input_email text)
 RETURNS TABLE(email text)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY
SELECT  c.email
FROM stripe.customers c
WHERE c.email = input_email;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.get_user_email_by_user_id(user_id uuid)
 RETURNS TABLE(email text)
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
BEGIN
  RETURN QUERY SELECT au.email::text FROM auth.users au WHERE au.id = user_id;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.handle_new_user()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
BEGIN
  INSERT INTO public.users (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.insert_secret(name text, secret text)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
begin
  return vault.create_secret(secret, name);
end;
$function$
;

CREATE OR REPLACE FUNCTION public.match_vectors(query_embedding vector, match_count integer, p_brain_id uuid)
 RETURNS TABLE(id uuid, brain_id uuid, content text, metadata jsonb, embedding vector, similarity double precision)
 LANGUAGE plpgsql
AS $function$
#variable_conflict use_column
BEGIN
    RETURN QUERY
    SELECT
        vectors.id,
        brains_vectors.brain_id,
        vectors.content,
        vectors.metadata,
        vectors.embedding,
        1 - (vectors.embedding <=> query_embedding) AS similarity
    FROM
        vectors
    INNER JOIN
        brains_vectors ON vectors.id = brains_vectors.vector_id
    WHERE brains_vectors.brain_id = p_brain_id
    ORDER BY
        vectors.embedding <=> query_embedding
    LIMIT match_count;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.read_secret(secret_name text)
 RETURNS text
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
declare
  secret text;
begin
  select decrypted_secret from vault.decrypted_secrets where name =
  secret_name into secret;
  return secret;
end;
$function$
;

CREATE OR REPLACE FUNCTION public.update_max_brains()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
DECLARE
    userEmail TEXT;
BEGIN
    SELECT email INTO userEmail FROM auth.users WHERE id = NEW.user_id;

    IF userEmail LIKE '%@theodo.fr' THEN
        -- Ensure the models column is initialized as an array if null
        IF NEW.models IS NULL THEN
            NEW.models := '[]'::jsonb;
        END IF;

        -- Add gpt-4 if not present
        IF NOT NEW.models ? 'gpt-4' THEN
            NEW.models := NEW.models || '["gpt-4"]'::jsonb;
        END IF;

        -- Add gpt-3.5-turbo if not present
        IF NOT NEW.models ? 'gpt-3.5-turbo' THEN
            NEW.models := NEW.models || '["gpt-3.5-turbo"]'::jsonb;
        END IF;

        -- Add gpt-3.5-turbo-16k if not present
        IF NOT NEW.models ? 'gpt-3.5-turbo-16k' THEN
            NEW.models := NEW.models || '["gpt-3.5-turbo-16k"]'::jsonb;
        END IF;

        UPDATE user_settings
        SET 
            max_brains = 30,
            max_brain_size = 10000000,
            models = NEW.models
        WHERE user_id = NEW.user_id;
    END IF;

    RETURN NULL;  -- for AFTER triggers, the return value is ignored
END;
$function$
;

CREATE OR REPLACE FUNCTION public.update_max_brains_theodo()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
AS $function$
DECLARE
    userEmail TEXT;
    allowedDomains TEXT[] := ARRAY['@theodo.fr', '@theodo.com', '@theodo.co.uk', '@bam.tech', '@padok.fr', '@sicara.fr', '@hokla.com', '@sipios.com'];
BEGIN
    SELECT email INTO userEmail FROM auth.users WHERE id = NEW.user_id;

    IF userEmail LIKE ANY(allowedDomains) THEN
        -- Ensure the models column is initialized as an array if null
        IF NEW.models IS NULL THEN
            NEW.models := '[]'::jsonb;
        END IF;

        -- Add gpt-4 if not present
        IF NOT NEW.models ? 'gpt-4' THEN
            NEW.models := NEW.models || '["gpt-4"]'::jsonb;
        END IF;

        -- Add gpt-3.5-turbo if not present
        IF NOT NEW.models ? 'gpt-3.5-turbo' THEN
            NEW.models := NEW.models || '["gpt-3.5-turbo"]'::jsonb;
        END IF;

        -- Add gpt-3.5-turbo-16k if not present
        IF NOT NEW.models ? 'gpt-3.5-turbo-16k' THEN
            NEW.models := NEW.models || '["gpt-3.5-turbo-16k"]'::jsonb;
        END IF;

        UPDATE user_settings
        SET 
            max_brains = 30,
            max_brain_size = 100000000,

            models = NEW.models
        WHERE user_id = NEW.user_id;
    END IF;

    RETURN NULL;  -- for AFTER triggers, the return value is ignored
END;
$function$
;

CREATE OR REPLACE FUNCTION public.update_user_settings()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF NEW.email LIKE '%@theodo.fr' THEN
        -- This checks if the models key is present and is of type jsonb array, 
        -- if not it initializes it with an empty array.
        IF NEW.models IS NULL OR NOT jsonb_typeof(NEW.models) = 'array' THEN
            NEW.models := '[]'::jsonb;
        END IF;

        -- Append new values to the JSONB array. 
        -- This does not check for duplicates, so you might get repeated values.
        NEW.models := NEW.models || '["gpt-4", "gpt-3.5-turbo"]'::jsonb;
    END IF;
    RETURN NEW;
END;
$function$
;

grant delete on table "public"."api_brain_definition" to "anon";

grant insert on table "public"."api_brain_definition" to "anon";

grant references on table "public"."api_brain_definition" to "anon";

grant select on table "public"."api_brain_definition" to "anon";

grant trigger on table "public"."api_brain_definition" to "anon";

grant truncate on table "public"."api_brain_definition" to "anon";

grant update on table "public"."api_brain_definition" to "anon";

grant delete on table "public"."api_brain_definition" to "authenticated";

grant insert on table "public"."api_brain_definition" to "authenticated";

grant references on table "public"."api_brain_definition" to "authenticated";

grant select on table "public"."api_brain_definition" to "authenticated";

grant trigger on table "public"."api_brain_definition" to "authenticated";

grant truncate on table "public"."api_brain_definition" to "authenticated";

grant update on table "public"."api_brain_definition" to "authenticated";

grant delete on table "public"."api_brain_definition" to "service_role";

grant insert on table "public"."api_brain_definition" to "service_role";

grant references on table "public"."api_brain_definition" to "service_role";

grant select on table "public"."api_brain_definition" to "service_role";

grant trigger on table "public"."api_brain_definition" to "service_role";

grant truncate on table "public"."api_brain_definition" to "service_role";

grant update on table "public"."api_brain_definition" to "service_role";

grant delete on table "public"."api_keys" to "anon";

grant insert on table "public"."api_keys" to "anon";

grant references on table "public"."api_keys" to "anon";

grant select on table "public"."api_keys" to "anon";

grant trigger on table "public"."api_keys" to "anon";

grant truncate on table "public"."api_keys" to "anon";

grant update on table "public"."api_keys" to "anon";

grant delete on table "public"."api_keys" to "authenticated";

grant insert on table "public"."api_keys" to "authenticated";

grant references on table "public"."api_keys" to "authenticated";

grant select on table "public"."api_keys" to "authenticated";

grant trigger on table "public"."api_keys" to "authenticated";

grant truncate on table "public"."api_keys" to "authenticated";

grant update on table "public"."api_keys" to "authenticated";

grant delete on table "public"."api_keys" to "service_role";

grant insert on table "public"."api_keys" to "service_role";

grant references on table "public"."api_keys" to "service_role";

grant select on table "public"."api_keys" to "service_role";

grant trigger on table "public"."api_keys" to "service_role";

grant truncate on table "public"."api_keys" to "service_role";

grant update on table "public"."api_keys" to "service_role";

grant delete on table "public"."brain_subscription_invitations" to "anon";

grant insert on table "public"."brain_subscription_invitations" to "anon";

grant references on table "public"."brain_subscription_invitations" to "anon";

grant select on table "public"."brain_subscription_invitations" to "anon";

grant trigger on table "public"."brain_subscription_invitations" to "anon";

grant truncate on table "public"."brain_subscription_invitations" to "anon";

grant update on table "public"."brain_subscription_invitations" to "anon";

grant delete on table "public"."brain_subscription_invitations" to "authenticated";

grant insert on table "public"."brain_subscription_invitations" to "authenticated";

grant references on table "public"."brain_subscription_invitations" to "authenticated";

grant select on table "public"."brain_subscription_invitations" to "authenticated";

grant trigger on table "public"."brain_subscription_invitations" to "authenticated";

grant truncate on table "public"."brain_subscription_invitations" to "authenticated";

grant update on table "public"."brain_subscription_invitations" to "authenticated";

grant delete on table "public"."brain_subscription_invitations" to "service_role";

grant insert on table "public"."brain_subscription_invitations" to "service_role";

grant references on table "public"."brain_subscription_invitations" to "service_role";

grant select on table "public"."brain_subscription_invitations" to "service_role";

grant trigger on table "public"."brain_subscription_invitations" to "service_role";

grant truncate on table "public"."brain_subscription_invitations" to "service_role";

grant update on table "public"."brain_subscription_invitations" to "service_role";

grant delete on table "public"."brains" to "anon";

grant insert on table "public"."brains" to "anon";

grant references on table "public"."brains" to "anon";

grant select on table "public"."brains" to "anon";

grant trigger on table "public"."brains" to "anon";

grant truncate on table "public"."brains" to "anon";

grant update on table "public"."brains" to "anon";

grant delete on table "public"."brains" to "authenticated";

grant insert on table "public"."brains" to "authenticated";

grant references on table "public"."brains" to "authenticated";

grant select on table "public"."brains" to "authenticated";

grant trigger on table "public"."brains" to "authenticated";

grant truncate on table "public"."brains" to "authenticated";

grant update on table "public"."brains" to "authenticated";

grant delete on table "public"."brains" to "service_role";

grant insert on table "public"."brains" to "service_role";

grant references on table "public"."brains" to "service_role";

grant select on table "public"."brains" to "service_role";

grant trigger on table "public"."brains" to "service_role";

grant truncate on table "public"."brains" to "service_role";

grant update on table "public"."brains" to "service_role";

grant delete on table "public"."brains_users" to "anon";

grant insert on table "public"."brains_users" to "anon";

grant references on table "public"."brains_users" to "anon";

grant select on table "public"."brains_users" to "anon";

grant trigger on table "public"."brains_users" to "anon";

grant truncate on table "public"."brains_users" to "anon";

grant update on table "public"."brains_users" to "anon";

grant delete on table "public"."brains_users" to "authenticated";

grant insert on table "public"."brains_users" to "authenticated";

grant references on table "public"."brains_users" to "authenticated";

grant select on table "public"."brains_users" to "authenticated";

grant trigger on table "public"."brains_users" to "authenticated";

grant truncate on table "public"."brains_users" to "authenticated";

grant update on table "public"."brains_users" to "authenticated";

grant delete on table "public"."brains_users" to "service_role";

grant insert on table "public"."brains_users" to "service_role";

grant references on table "public"."brains_users" to "service_role";

grant select on table "public"."brains_users" to "service_role";

grant trigger on table "public"."brains_users" to "service_role";

grant truncate on table "public"."brains_users" to "service_role";

grant update on table "public"."brains_users" to "service_role";

grant delete on table "public"."brains_vectors" to "anon";

grant insert on table "public"."brains_vectors" to "anon";

grant references on table "public"."brains_vectors" to "anon";

grant select on table "public"."brains_vectors" to "anon";

grant trigger on table "public"."brains_vectors" to "anon";

grant truncate on table "public"."brains_vectors" to "anon";

grant update on table "public"."brains_vectors" to "anon";

grant delete on table "public"."brains_vectors" to "authenticated";

grant insert on table "public"."brains_vectors" to "authenticated";

grant references on table "public"."brains_vectors" to "authenticated";

grant select on table "public"."brains_vectors" to "authenticated";

grant trigger on table "public"."brains_vectors" to "authenticated";

grant truncate on table "public"."brains_vectors" to "authenticated";

grant update on table "public"."brains_vectors" to "authenticated";

grant delete on table "public"."brains_vectors" to "service_role";

grant insert on table "public"."brains_vectors" to "service_role";

grant references on table "public"."brains_vectors" to "service_role";

grant select on table "public"."brains_vectors" to "service_role";

grant trigger on table "public"."brains_vectors" to "service_role";

grant truncate on table "public"."brains_vectors" to "service_role";

grant update on table "public"."brains_vectors" to "service_role";

grant delete on table "public"."chat_history" to "anon";

grant insert on table "public"."chat_history" to "anon";

grant references on table "public"."chat_history" to "anon";

grant select on table "public"."chat_history" to "anon";

grant trigger on table "public"."chat_history" to "anon";

grant truncate on table "public"."chat_history" to "anon";

grant update on table "public"."chat_history" to "anon";

grant delete on table "public"."chat_history" to "authenticated";

grant insert on table "public"."chat_history" to "authenticated";

grant references on table "public"."chat_history" to "authenticated";

grant select on table "public"."chat_history" to "authenticated";

grant trigger on table "public"."chat_history" to "authenticated";

grant truncate on table "public"."chat_history" to "authenticated";

grant update on table "public"."chat_history" to "authenticated";

grant delete on table "public"."chat_history" to "service_role";

grant insert on table "public"."chat_history" to "service_role";

grant references on table "public"."chat_history" to "service_role";

grant select on table "public"."chat_history" to "service_role";

grant trigger on table "public"."chat_history" to "service_role";

grant truncate on table "public"."chat_history" to "service_role";

grant update on table "public"."chat_history" to "service_role";

grant delete on table "public"."chats" to "anon";

grant insert on table "public"."chats" to "anon";

grant references on table "public"."chats" to "anon";

grant select on table "public"."chats" to "anon";

grant trigger on table "public"."chats" to "anon";

grant truncate on table "public"."chats" to "anon";

grant update on table "public"."chats" to "anon";

grant delete on table "public"."chats" to "authenticated";

grant insert on table "public"."chats" to "authenticated";

grant references on table "public"."chats" to "authenticated";

grant select on table "public"."chats" to "authenticated";

grant trigger on table "public"."chats" to "authenticated";

grant truncate on table "public"."chats" to "authenticated";

grant update on table "public"."chats" to "authenticated";

grant delete on table "public"."chats" to "service_role";

grant insert on table "public"."chats" to "service_role";

grant references on table "public"."chats" to "service_role";

grant select on table "public"."chats" to "service_role";

grant trigger on table "public"."chats" to "service_role";

grant truncate on table "public"."chats" to "service_role";

grant update on table "public"."chats" to "service_role";

grant delete on table "public"."composite_brain_connections" to "anon";

grant insert on table "public"."composite_brain_connections" to "anon";

grant references on table "public"."composite_brain_connections" to "anon";

grant select on table "public"."composite_brain_connections" to "anon";

grant trigger on table "public"."composite_brain_connections" to "anon";

grant truncate on table "public"."composite_brain_connections" to "anon";

grant update on table "public"."composite_brain_connections" to "anon";

grant delete on table "public"."composite_brain_connections" to "authenticated";

grant insert on table "public"."composite_brain_connections" to "authenticated";

grant references on table "public"."composite_brain_connections" to "authenticated";

grant select on table "public"."composite_brain_connections" to "authenticated";

grant trigger on table "public"."composite_brain_connections" to "authenticated";

grant truncate on table "public"."composite_brain_connections" to "authenticated";

grant update on table "public"."composite_brain_connections" to "authenticated";

grant delete on table "public"."composite_brain_connections" to "service_role";

grant insert on table "public"."composite_brain_connections" to "service_role";

grant references on table "public"."composite_brain_connections" to "service_role";

grant select on table "public"."composite_brain_connections" to "service_role";

grant trigger on table "public"."composite_brain_connections" to "service_role";

grant truncate on table "public"."composite_brain_connections" to "service_role";

grant update on table "public"."composite_brain_connections" to "service_role";

grant delete on table "public"."knowledge" to "anon";

grant insert on table "public"."knowledge" to "anon";

grant references on table "public"."knowledge" to "anon";

grant select on table "public"."knowledge" to "anon";

grant trigger on table "public"."knowledge" to "anon";

grant truncate on table "public"."knowledge" to "anon";

grant update on table "public"."knowledge" to "anon";

grant delete on table "public"."knowledge" to "authenticated";

grant insert on table "public"."knowledge" to "authenticated";

grant references on table "public"."knowledge" to "authenticated";

grant select on table "public"."knowledge" to "authenticated";

grant trigger on table "public"."knowledge" to "authenticated";

grant truncate on table "public"."knowledge" to "authenticated";

grant update on table "public"."knowledge" to "authenticated";

grant delete on table "public"."knowledge" to "service_role";

grant insert on table "public"."knowledge" to "service_role";

grant references on table "public"."knowledge" to "service_role";

grant select on table "public"."knowledge" to "service_role";

grant trigger on table "public"."knowledge" to "service_role";

grant truncate on table "public"."knowledge" to "service_role";

grant update on table "public"."knowledge" to "service_role";

grant delete on table "public"."knowledge_vectors" to "anon";

grant insert on table "public"."knowledge_vectors" to "anon";

grant references on table "public"."knowledge_vectors" to "anon";

grant select on table "public"."knowledge_vectors" to "anon";

grant trigger on table "public"."knowledge_vectors" to "anon";

grant truncate on table "public"."knowledge_vectors" to "anon";

grant update on table "public"."knowledge_vectors" to "anon";

grant delete on table "public"."knowledge_vectors" to "authenticated";

grant insert on table "public"."knowledge_vectors" to "authenticated";

grant references on table "public"."knowledge_vectors" to "authenticated";

grant select on table "public"."knowledge_vectors" to "authenticated";

grant trigger on table "public"."knowledge_vectors" to "authenticated";

grant truncate on table "public"."knowledge_vectors" to "authenticated";

grant update on table "public"."knowledge_vectors" to "authenticated";

grant delete on table "public"."knowledge_vectors" to "service_role";

grant insert on table "public"."knowledge_vectors" to "service_role";

grant references on table "public"."knowledge_vectors" to "service_role";

grant select on table "public"."knowledge_vectors" to "service_role";

grant trigger on table "public"."knowledge_vectors" to "service_role";

grant truncate on table "public"."knowledge_vectors" to "service_role";

grant update on table "public"."knowledge_vectors" to "service_role";

grant delete on table "public"."migrations" to "anon";

grant insert on table "public"."migrations" to "anon";

grant references on table "public"."migrations" to "anon";

grant select on table "public"."migrations" to "anon";

grant trigger on table "public"."migrations" to "anon";

grant truncate on table "public"."migrations" to "anon";

grant update on table "public"."migrations" to "anon";

grant delete on table "public"."migrations" to "authenticated";

grant insert on table "public"."migrations" to "authenticated";

grant references on table "public"."migrations" to "authenticated";

grant select on table "public"."migrations" to "authenticated";

grant trigger on table "public"."migrations" to "authenticated";

grant truncate on table "public"."migrations" to "authenticated";

grant update on table "public"."migrations" to "authenticated";

grant delete on table "public"."migrations" to "service_role";

grant insert on table "public"."migrations" to "service_role";

grant references on table "public"."migrations" to "service_role";

grant select on table "public"."migrations" to "service_role";

grant trigger on table "public"."migrations" to "service_role";

grant truncate on table "public"."migrations" to "service_role";

grant update on table "public"."migrations" to "service_role";

grant delete on table "public"."notifications" to "anon";

grant insert on table "public"."notifications" to "anon";

grant references on table "public"."notifications" to "anon";

grant select on table "public"."notifications" to "anon";

grant trigger on table "public"."notifications" to "anon";

grant truncate on table "public"."notifications" to "anon";

grant update on table "public"."notifications" to "anon";

grant delete on table "public"."notifications" to "authenticated";

grant insert on table "public"."notifications" to "authenticated";

grant references on table "public"."notifications" to "authenticated";

grant select on table "public"."notifications" to "authenticated";

grant trigger on table "public"."notifications" to "authenticated";

grant truncate on table "public"."notifications" to "authenticated";

grant update on table "public"."notifications" to "authenticated";

grant delete on table "public"."notifications" to "service_role";

grant insert on table "public"."notifications" to "service_role";

grant references on table "public"."notifications" to "service_role";

grant select on table "public"."notifications" to "service_role";

grant trigger on table "public"."notifications" to "service_role";

grant truncate on table "public"."notifications" to "service_role";

grant update on table "public"."notifications" to "service_role";

grant delete on table "public"."onboardings" to "anon";

grant insert on table "public"."onboardings" to "anon";

grant references on table "public"."onboardings" to "anon";

grant select on table "public"."onboardings" to "anon";

grant trigger on table "public"."onboardings" to "anon";

grant truncate on table "public"."onboardings" to "anon";

grant update on table "public"."onboardings" to "anon";

grant delete on table "public"."onboardings" to "authenticated";

grant insert on table "public"."onboardings" to "authenticated";

grant references on table "public"."onboardings" to "authenticated";

grant select on table "public"."onboardings" to "authenticated";

grant trigger on table "public"."onboardings" to "authenticated";

grant truncate on table "public"."onboardings" to "authenticated";

grant update on table "public"."onboardings" to "authenticated";

grant delete on table "public"."onboardings" to "service_role";

grant insert on table "public"."onboardings" to "service_role";

grant references on table "public"."onboardings" to "service_role";

grant select on table "public"."onboardings" to "service_role";

grant trigger on table "public"."onboardings" to "service_role";

grant truncate on table "public"."onboardings" to "service_role";

grant update on table "public"."onboardings" to "service_role";

grant delete on table "public"."prompts" to "anon";

grant insert on table "public"."prompts" to "anon";

grant references on table "public"."prompts" to "anon";

grant select on table "public"."prompts" to "anon";

grant trigger on table "public"."prompts" to "anon";

grant truncate on table "public"."prompts" to "anon";

grant update on table "public"."prompts" to "anon";

grant delete on table "public"."prompts" to "authenticated";

grant insert on table "public"."prompts" to "authenticated";

grant references on table "public"."prompts" to "authenticated";

grant select on table "public"."prompts" to "authenticated";

grant trigger on table "public"."prompts" to "authenticated";

grant truncate on table "public"."prompts" to "authenticated";

grant update on table "public"."prompts" to "authenticated";

grant delete on table "public"."prompts" to "service_role";

grant insert on table "public"."prompts" to "service_role";

grant references on table "public"."prompts" to "service_role";

grant select on table "public"."prompts" to "service_role";

grant trigger on table "public"."prompts" to "service_role";

grant truncate on table "public"."prompts" to "service_role";

grant update on table "public"."prompts" to "service_role";

grant delete on table "public"."stats" to "anon";

grant insert on table "public"."stats" to "anon";

grant references on table "public"."stats" to "anon";

grant select on table "public"."stats" to "anon";

grant trigger on table "public"."stats" to "anon";

grant truncate on table "public"."stats" to "anon";

grant update on table "public"."stats" to "anon";

grant delete on table "public"."stats" to "authenticated";

grant insert on table "public"."stats" to "authenticated";

grant references on table "public"."stats" to "authenticated";

grant select on table "public"."stats" to "authenticated";

grant trigger on table "public"."stats" to "authenticated";

grant truncate on table "public"."stats" to "authenticated";

grant update on table "public"."stats" to "authenticated";

grant delete on table "public"."stats" to "service_role";

grant insert on table "public"."stats" to "service_role";

grant references on table "public"."stats" to "service_role";

grant select on table "public"."stats" to "service_role";

grant trigger on table "public"."stats" to "service_role";

grant truncate on table "public"."stats" to "service_role";

grant update on table "public"."stats" to "service_role";

grant delete on table "public"."summaries" to "anon";

grant insert on table "public"."summaries" to "anon";

grant references on table "public"."summaries" to "anon";

grant select on table "public"."summaries" to "anon";

grant trigger on table "public"."summaries" to "anon";

grant truncate on table "public"."summaries" to "anon";

grant update on table "public"."summaries" to "anon";

grant delete on table "public"."summaries" to "authenticated";

grant insert on table "public"."summaries" to "authenticated";

grant references on table "public"."summaries" to "authenticated";

grant select on table "public"."summaries" to "authenticated";

grant trigger on table "public"."summaries" to "authenticated";

grant truncate on table "public"."summaries" to "authenticated";

grant update on table "public"."summaries" to "authenticated";

grant delete on table "public"."summaries" to "service_role";

grant insert on table "public"."summaries" to "service_role";

grant references on table "public"."summaries" to "service_role";

grant select on table "public"."summaries" to "service_role";

grant trigger on table "public"."summaries" to "service_role";

grant truncate on table "public"."summaries" to "service_role";

grant update on table "public"."summaries" to "service_role";

grant delete on table "public"."user_daily_usage" to "anon";

grant insert on table "public"."user_daily_usage" to "anon";

grant references on table "public"."user_daily_usage" to "anon";

grant select on table "public"."user_daily_usage" to "anon";

grant trigger on table "public"."user_daily_usage" to "anon";

grant truncate on table "public"."user_daily_usage" to "anon";

grant update on table "public"."user_daily_usage" to "anon";

grant delete on table "public"."user_daily_usage" to "authenticated";

grant insert on table "public"."user_daily_usage" to "authenticated";

grant references on table "public"."user_daily_usage" to "authenticated";

grant select on table "public"."user_daily_usage" to "authenticated";

grant trigger on table "public"."user_daily_usage" to "authenticated";

grant truncate on table "public"."user_daily_usage" to "authenticated";

grant update on table "public"."user_daily_usage" to "authenticated";

grant delete on table "public"."user_daily_usage" to "service_role";

grant insert on table "public"."user_daily_usage" to "service_role";

grant references on table "public"."user_daily_usage" to "service_role";

grant select on table "public"."user_daily_usage" to "service_role";

grant trigger on table "public"."user_daily_usage" to "service_role";

grant truncate on table "public"."user_daily_usage" to "service_role";

grant update on table "public"."user_daily_usage" to "service_role";

grant delete on table "public"."user_identity" to "anon";

grant insert on table "public"."user_identity" to "anon";

grant references on table "public"."user_identity" to "anon";

grant select on table "public"."user_identity" to "anon";

grant trigger on table "public"."user_identity" to "anon";

grant truncate on table "public"."user_identity" to "anon";

grant update on table "public"."user_identity" to "anon";

grant delete on table "public"."user_identity" to "authenticated";

grant insert on table "public"."user_identity" to "authenticated";

grant references on table "public"."user_identity" to "authenticated";

grant select on table "public"."user_identity" to "authenticated";

grant trigger on table "public"."user_identity" to "authenticated";

grant truncate on table "public"."user_identity" to "authenticated";

grant update on table "public"."user_identity" to "authenticated";

grant delete on table "public"."user_identity" to "service_role";

grant insert on table "public"."user_identity" to "service_role";

grant references on table "public"."user_identity" to "service_role";

grant select on table "public"."user_identity" to "service_role";

grant trigger on table "public"."user_identity" to "service_role";

grant truncate on table "public"."user_identity" to "service_role";

grant update on table "public"."user_identity" to "service_role";

grant delete on table "public"."user_settings" to "anon";

grant insert on table "public"."user_settings" to "anon";

grant references on table "public"."user_settings" to "anon";

grant select on table "public"."user_settings" to "anon";

grant trigger on table "public"."user_settings" to "anon";

grant truncate on table "public"."user_settings" to "anon";

grant update on table "public"."user_settings" to "anon";

grant delete on table "public"."user_settings" to "authenticated";

grant insert on table "public"."user_settings" to "authenticated";

grant references on table "public"."user_settings" to "authenticated";

grant select on table "public"."user_settings" to "authenticated";

grant trigger on table "public"."user_settings" to "authenticated";

grant truncate on table "public"."user_settings" to "authenticated";

grant update on table "public"."user_settings" to "authenticated";

grant delete on table "public"."user_settings" to "service_role";

grant insert on table "public"."user_settings" to "service_role";

grant references on table "public"."user_settings" to "service_role";

grant select on table "public"."user_settings" to "service_role";

grant trigger on table "public"."user_settings" to "service_role";

grant truncate on table "public"."user_settings" to "service_role";

grant update on table "public"."user_settings" to "service_role";

grant delete on table "public"."users" to "anon";

grant insert on table "public"."users" to "anon";

grant references on table "public"."users" to "anon";

grant select on table "public"."users" to "anon";

grant trigger on table "public"."users" to "anon";

grant truncate on table "public"."users" to "anon";

grant update on table "public"."users" to "anon";

grant delete on table "public"."users" to "authenticated";

grant insert on table "public"."users" to "authenticated";

grant references on table "public"."users" to "authenticated";

grant select on table "public"."users" to "authenticated";

grant trigger on table "public"."users" to "authenticated";

grant truncate on table "public"."users" to "authenticated";

grant update on table "public"."users" to "authenticated";

grant delete on table "public"."users" to "service_role";

grant insert on table "public"."users" to "service_role";

grant references on table "public"."users" to "service_role";

grant select on table "public"."users" to "service_role";

grant trigger on table "public"."users" to "service_role";

grant truncate on table "public"."users" to "service_role";

grant update on table "public"."users" to "service_role";

grant delete on table "public"."users_old" to "anon";

grant insert on table "public"."users_old" to "anon";

grant references on table "public"."users_old" to "anon";

grant select on table "public"."users_old" to "anon";

grant trigger on table "public"."users_old" to "anon";

grant truncate on table "public"."users_old" to "anon";

grant update on table "public"."users_old" to "anon";

grant delete on table "public"."users_old" to "authenticated";

grant insert on table "public"."users_old" to "authenticated";

grant references on table "public"."users_old" to "authenticated";

grant select on table "public"."users_old" to "authenticated";

grant trigger on table "public"."users_old" to "authenticated";

grant truncate on table "public"."users_old" to "authenticated";

grant update on table "public"."users_old" to "authenticated";

grant delete on table "public"."users_old" to "service_role";

grant insert on table "public"."users_old" to "service_role";

grant references on table "public"."users_old" to "service_role";

grant select on table "public"."users_old" to "service_role";

grant trigger on table "public"."users_old" to "service_role";

grant truncate on table "public"."users_old" to "service_role";

grant update on table "public"."users_old" to "service_role";

grant delete on table "public"."vectors" to "anon";

grant insert on table "public"."vectors" to "anon";

grant references on table "public"."vectors" to "anon";

grant select on table "public"."vectors" to "anon";

grant trigger on table "public"."vectors" to "anon";

grant truncate on table "public"."vectors" to "anon";

grant update on table "public"."vectors" to "anon";

grant delete on table "public"."vectors" to "authenticated";

grant insert on table "public"."vectors" to "authenticated";

grant references on table "public"."vectors" to "authenticated";

grant select on table "public"."vectors" to "authenticated";

grant trigger on table "public"."vectors" to "authenticated";

grant truncate on table "public"."vectors" to "authenticated";

grant update on table "public"."vectors" to "authenticated";

grant delete on table "public"."vectors" to "service_role";

grant insert on table "public"."vectors" to "service_role";

grant references on table "public"."vectors" to "service_role";

grant select on table "public"."vectors" to "service_role";

grant trigger on table "public"."vectors" to "service_role";

grant truncate on table "public"."vectors" to "service_role";

grant update on table "public"."vectors" to "service_role";

grant delete on table "public"."vectors_old" to "anon";

grant insert on table "public"."vectors_old" to "anon";

grant references on table "public"."vectors_old" to "anon";

grant select on table "public"."vectors_old" to "anon";

grant trigger on table "public"."vectors_old" to "anon";

grant truncate on table "public"."vectors_old" to "anon";

grant update on table "public"."vectors_old" to "anon";

grant delete on table "public"."vectors_old" to "authenticated";

grant insert on table "public"."vectors_old" to "authenticated";

grant references on table "public"."vectors_old" to "authenticated";

grant select on table "public"."vectors_old" to "authenticated";

grant trigger on table "public"."vectors_old" to "authenticated";

grant truncate on table "public"."vectors_old" to "authenticated";

grant update on table "public"."vectors_old" to "authenticated";

grant delete on table "public"."vectors_old" to "service_role";

grant insert on table "public"."vectors_old" to "service_role";

grant references on table "public"."vectors_old" to "service_role";

grant select on table "public"."vectors_old" to "service_role";

grant trigger on table "public"."vectors_old" to "service_role";

grant truncate on table "public"."vectors_old" to "service_role";

grant update on table "public"."vectors_old" to "service_role";


create schema if not exists "stripe";


-- Create users table
CREATE TABLE IF NOT EXISTS user_daily_usage(
    user_id UUID REFERENCES auth.users (id),
    email TEXT,
    date TEXT,
    daily_requests_count INT,
    PRIMARY KEY (user_id, date)
);

-- Create chats table
CREATE TABLE IF NOT EXISTS chats(
    chat_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users (id),
    creation_time TIMESTAMP DEFAULT current_timestamp,
    history JSONB,
    chat_name TEXT
);


-- Create vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create vectors table
CREATE TABLE IF NOT EXISTS vectors (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    content TEXT,
    file_sha1 TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);

-- Create function to match vectors
CREATE OR REPLACE FUNCTION match_vectors(query_embedding VECTOR(1536), match_count INT, p_brain_id UUID)
RETURNS TABLE(
    id UUID,
    brain_id UUID,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536),
    similarity FLOAT
) LANGUAGE plpgsql AS $$
#variable_conflict use_column
BEGIN
    RETURN QUERY
    SELECT
        vectors.id,
        brains_vectors.brain_id,
        vectors.content,
        vectors.metadata,
        vectors.embedding,
        1 - (vectors.embedding <=> query_embedding) AS similarity
    FROM
        vectors
    INNER JOIN
        brains_vectors ON vectors.id = brains_vectors.vector_id
    WHERE brains_vectors.brain_id = p_brain_id
    ORDER BY
        vectors.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create stats table
CREATE TABLE IF NOT EXISTS stats (
    time TIMESTAMP,
    chat BOOLEAN,
    embedding BOOLEAN,
    details TEXT,
    metadata JSONB,
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY
);

-- Create summaries table
CREATE TABLE IF NOT EXISTS summaries (
    id BIGSERIAL PRIMARY KEY,
    document_id UUID REFERENCES vectors(id),
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);

-- Create function to match summaries
CREATE OR REPLACE FUNCTION match_summaries(query_embedding VECTOR(1536), match_count INT, match_threshold FLOAT)
RETURNS TABLE(
    id BIGINT,
    document_id UUID,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536),
    similarity FLOAT
) LANGUAGE plpgsql AS $$
#variable_conflict use_column
BEGIN
    RETURN QUERY
    SELECT
        id,
        document_id,
        content,
        metadata,
        embedding,
        1 - (summaries.embedding <=> query_embedding) AS similarity
    FROM
        summaries
    WHERE 1 - (summaries.embedding <=> query_embedding) > match_threshold
    ORDER BY
        summaries.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create api_keys table
CREATE TABLE IF NOT EXISTS api_keys(
    key_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users (id),
    name TEXT DEFAULT 'API_KEY', 
    days INT DEFAULT 30,
    only_chat BOOLEAN DEFAULT false,
    api_key TEXT UNIQUE,
    creation_time TIMESTAMP DEFAULT current_timestamp,
    deleted_time TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

--- Create prompts table
CREATE TABLE IF NOT EXISTS prompts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    status VARCHAR(255) DEFAULT 'private'
);

DO $$ 
BEGIN 
IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'brain_type_enum') THEN
  -- Create the ENUM type 'brain_type' if it doesn't exist
  CREATE TYPE brain_type_enum AS ENUM ('doc', 'api', 'composite');
END IF;
END $$;

--- Create brains table
CREATE TABLE IF NOT EXISTS brains (
  brain_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  status TEXT,
  description TEXT,
  model TEXT,
  max_tokens INT,
  temperature FLOAT,
  prompt_id UUID REFERENCES prompts(id),
  last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  brain_type brain_type_enum DEFAULT 'doc'
);


-- Create chat_history table
CREATE TABLE IF NOT EXISTS chat_history (
    message_id UUID DEFAULT uuid_generate_v4(),
    chat_id UUID REFERENCES chats(chat_id),
    user_message TEXT,
    assistant TEXT,
    message_time TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (chat_id, message_id),
    prompt_id UUID REFERENCES prompts(id),
    brain_id UUID REFERENCES brains(brain_id)
);

-- Create notification table

CREATE TABLE IF NOT EXISTS notifications (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  chat_id UUID REFERENCES chats(chat_id),
  message TEXT,
  action VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL
);


-- Create brains X users table
CREATE TABLE IF NOT EXISTS brains_users (
  brain_id UUID,
  user_id UUID,
  rights VARCHAR(255),
  default_brain BOOLEAN DEFAULT false,
  PRIMARY KEY (brain_id, user_id),
  FOREIGN KEY (user_id) REFERENCES auth.users (id),
  FOREIGN KEY (brain_id) REFERENCES brains (brain_id)
);

-- Create brains X vectors table
CREATE TABLE IF NOT EXISTS brains_vectors (
  brain_id UUID,
  vector_id UUID,
  file_sha1 TEXT,
  PRIMARY KEY (brain_id, vector_id),
  FOREIGN KEY (vector_id) REFERENCES vectors (id),
  FOREIGN KEY (brain_id) REFERENCES brains (brain_id)
);

-- Create brains X vectors table
CREATE TABLE IF NOT EXISTS brain_subscription_invitations (
  brain_id UUID,
  email VARCHAR(255),
  rights VARCHAR(255),
  PRIMARY KEY (brain_id, email),
  FOREIGN KEY (brain_id) REFERENCES brains (brain_id)
);

-- Table for storing the relationship between brains for composite brains
CREATE TABLE IF NOT EXISTS composite_brain_connections (
  composite_brain_id UUID NOT NULL REFERENCES brains(brain_id),
  connected_brain_id UUID NOT NULL REFERENCES brains(brain_id),
  PRIMARY KEY (composite_brain_id, connected_brain_id),
  CHECK (composite_brain_id != connected_brain_id)
);

--- Create user_identity table
CREATE TABLE IF NOT EXISTS user_identity (
  user_id UUID PRIMARY KEY,
  openai_api_key VARCHAR(255)
);

-- Create the new table with 6 columns
CREATE TABLE IF NOT EXISTS api_brain_definition (
    brain_id UUID REFERENCES brains(brain_id),
    method VARCHAR(255) CHECK (method IN ('GET', 'POST', 'PUT', 'DELETE')),
    url VARCHAR(255),
    params JSON,
    search_params JSON,
    secrets JSON
);

CREATE OR REPLACE FUNCTION public.get_user_email_by_user_id(user_id uuid)
RETURNS TABLE (email text)
SECURITY definer
AS $$
BEGIN
  RETURN QUERY SELECT au.email::text FROM auth.users au WHERE au.id = user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.get_user_id_by_user_email(user_email text)
RETURNS TABLE (user_id uuid)
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY SELECT au.id::uuid FROM auth.users au WHERE au.email = user_email;
END;
$$ LANGUAGE plpgsql;





CREATE TABLE IF NOT EXISTS user_settings (
  user_id UUID PRIMARY KEY,
  models JSONB DEFAULT '["gpt-3.5-turbo-1106","gpt-4"]'::jsonb,
  daily_chat_credit INT DEFAULT 300,
  max_brains INT DEFAULT 30,
  max_brain_size INT DEFAULT 100000000
);

-- knowledge table
CREATE TABLE IF NOT EXISTS knowledge (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  file_name TEXT,
  url TEXT,
  brain_id UUID NOT NULL REFERENCES brains(brain_id),
  extension TEXT NOT NULL,
  CHECK ((file_name IS NOT NULL AND url IS NULL) OR (file_name IS NULL AND url IS NOT NULL))
);


-- knowledge_vectors table
CREATE TABLE IF NOT EXISTS knowledge_vectors (
  knowledge_id UUID NOT NULL REFERENCES knowledge(id),
  vector_id UUID NOT NULL REFERENCES vectors(id),
  embedding_model TEXT NOT NULL,
  PRIMARY KEY (knowledge_id, vector_id, embedding_model)
);

-- Create the function to add user_id to the onboardings table
CREATE OR REPLACE FUNCTION public.create_user_onboarding() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.onboardings (user_id)
    VALUES (NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY definer;

-- Revoke all on function handle_new_user_onboarding() from PUBLIC;
REVOKE ALL ON FUNCTION create_user_onboarding() FROM PUBLIC;

-- Drop the trigger if it exists
DROP TRIGGER IF EXISTS create_user_onboarding_trigger ON auth.users;

-- Create the trigger on the insert into the auth.users table
CREATE TRIGGER create_user_onboarding_trigger
AFTER INSERT ON auth.users
FOR EACH ROW
EXECUTE FUNCTION public.create_user_onboarding();

-- Create the onboarding table
CREATE TABLE IF NOT EXISTS onboardings (
  user_id UUID NOT NULL REFERENCES auth.users (id),
  onboarding_a BOOLEAN NOT NULL DEFAULT true,
  onboarding_b1 BOOLEAN NOT NULL DEFAULT true,
  onboarding_b2 BOOLEAN NOT NULL DEFAULT true,
  onboarding_b3 BOOLEAN NOT NULL DEFAULT true,
  creation_time TIMESTAMP DEFAULT current_timestamp,
  PRIMARY KEY (user_id)
);


-- Stripe settings --
-- Create extension 'wrappers' if it doesn't exist
CREATE EXTENSION IF NOT EXISTS wrappers;

-- Create foreign data wrapper 'stripe_wrapper' if it doesn't exist
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 
    FROM information_schema.foreign_data_wrappers 
    WHERE foreign_data_wrapper_name = 'stripe_wrapper'
  ) THEN
    CREATE FOREIGN DATA WRAPPER stripe_wrapper
      HANDLER stripe_fdw_handler;
  END IF;
END $$;

-- Check if the server 'stripe_server' exists before creating it
DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_foreign_server WHERE srvname = 'stripe_server') THEN
    CREATE SERVER stripe_server
      FOREIGN DATA WRAPPER stripe_wrapper
      OPTIONS (
        api_key 'sk_test_51NtDTIJglvQxkJ1HVZHZHpKNAm48jAzKfJs93MjpKiML9YHy8G1YoKIf6SpcnGwRFWjmdS664A2Z2dn4LORWpo1P00qt6Jmy8G'  -- Replace with your Stripe API key
      );
  END IF;
END $$;

-- Create foreign table 'public.customers' if it doesn't exist
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_name = 'customers' 
  ) THEN
    CREATE FOREIGN TABLE public.customers (
      id text,
      email text,
      name text,
      description text,
      created timestamp,
      attrs jsonb
    )
    SERVER stripe_server
    OPTIONS (
      OBJECT 'customers',
      ROWID_COLUMN 'id'
    );
  END IF;
END $$;

-- Create table 'users' if it doesn't exist
CREATE TABLE IF NOT EXISTS public.users (
  id uuid REFERENCES auth.users NOT NULL PRIMARY KEY,
  email text
);

-- Create or replace function 'public.handle_new_user' 
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if the trigger 'on_auth_user_created' exists before creating it
DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'on_auth_user_created') THEN
    CREATE TRIGGER on_auth_user_created
      AFTER INSERT ON auth.users
      FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
  END IF;
END $$;

insert into
  storage.buckets (id, name)
values
  ('quivr', 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_0" ON storage.objects FOR INSERT TO anon WITH CHECK (bucket_id = 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_1" ON storage.objects FOR SELECT TO anon USING (bucket_id = 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_2" ON storage.objects FOR UPDATE TO anon USING (bucket_id = 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_3" ON storage.objects FOR DELETE TO anon USING (bucket_id = 'quivr');

-- Create functions for secrets in vault
CREATE OR REPLACE FUNCTION insert_secret(name text, secret text)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
begin
  return vault.create_secret(secret, name);
end;
$$;


create or replace function read_secret(secret_name text)
returns text
language plpgsql
security definer set search_path = public
as $$
declare
  secret text;
begin
  select decrypted_secret from vault.decrypted_secrets where name =
  secret_name into secret;
  return secret;
end;
$$;

create or replace function delete_secret(secret_name text)
returns text
language plpgsql
security definer set search_path = public
as $$
declare
 deleted_rows int;
begin
 delete from vault.decrypted_secrets where name = secret_name;
 get diagnostics deleted_rows = row_count;
 if deleted_rows = 0 then
   return false;
 else
   return true;
 end if;
end;
$$;

create schema if not exists extensions;

create table if not exists
  extensions.wrappers_fdw_stats ();

grant all on extensions.wrappers_fdw_stats to service_role;



