create sequence "public"."documents_id_seq";

drop function if exists "public"."get_premium_user"(input_email text);

drop function if exists "public"."update_max_brains"();

drop function if exists "public"."update_user_settings"();

drop function if exists "public"."match_summaries"(query_embedding vector, match_count integer, match_threshold double precision);

alter table "public"."vectors" drop constraint "vectors_pkey1";

drop index if exists "public"."vectors_pkey1";

create table "public"."documents" (
    "id" bigint not null default nextval('documents_id_seq'::regclass),
    "content" text,
    "metadata" jsonb,
    "embedding" vector(1536)
);


alter table "public"."brains" drop column "retrieval_algorithm";

alter table "public"."brains" add column "openai_api_key" text;

alter table "public"."brains" alter column "status" set default 'private'::text;

alter table "public"."brains_users" alter column "default_brain" set default false;

alter table "public"."brains_vectors" drop column "rights";

alter table "public"."user_settings" alter column "max_brain_size" set default 50000000;

alter table "public"."vectors" alter column "id" drop default;

alter sequence "public"."documents_id_seq" owned by "public"."documents"."id";

CREATE INDEX brains_vectors_brain_id_idx ON public.brains_vectors USING btree (brain_id);

CREATE INDEX brains_vectors_vector_id_idx ON public.brains_vectors USING btree (vector_id);

CREATE UNIQUE INDEX documents_pkey ON public.documents USING btree (id);

CREATE INDEX idx_brains_vectors_vector_id ON public.brains_vectors USING btree (vector_id);

CREATE INDEX idx_vectors_id ON public.vectors USING btree (id);

CREATE INDEX vectors_file_sha1_idx ON public.vectors USING btree (file_sha1);

CREATE INDEX vectors_id_idx ON public.vectors USING btree (id);

CREATE UNIQUE INDEX vectors_new_pkey ON public.vectors USING btree (id);

alter table "public"."documents" add constraint "documents_pkey" PRIMARY KEY using index "documents_pkey";

alter table "public"."vectors" add constraint "vectors_new_pkey" PRIMARY KEY using index "vectors_new_pkey";

alter table "public"."api_keys" add constraint "api_keys_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) not valid;

alter table "public"."api_keys" validate constraint "api_keys_user_id_fkey";

alter table "public"."brains_vectors" add constraint "brains_vectors_vector_id_fkey" FOREIGN KEY (vector_id) REFERENCES vectors(id) not valid;

alter table "public"."brains_vectors" validate constraint "brains_vectors_vector_id_fkey";

alter table "public"."knowledge_vectors" add constraint "knowledge_vectors_vector_id_fkey" FOREIGN KEY (vector_id) REFERENCES vectors(id) not valid;

alter table "public"."knowledge_vectors" validate constraint "knowledge_vectors_vector_id_fkey";

alter table "public"."summaries" add constraint "summaries_document_id_fkey" FOREIGN KEY (document_id) REFERENCES vectors(id) not valid;

alter table "public"."summaries" validate constraint "summaries_document_id_fkey";

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.match_documents(query_embedding vector, match_count integer)
 RETURNS TABLE(id bigint, content text, metadata jsonb, similarity double precision)
 LANGUAGE plpgsql
AS $function$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$function$
;

CREATE OR REPLACE FUNCTION public.match_summaries(query_embedding vector, match_count integer, match_threshold double precision)
 RETURNS TABLE(id bigint, document_id bigint, content text, metadata jsonb, embedding vector, similarity double precision)
 LANGUAGE plpgsql
AS $function$
    # variable_conflict use_column
BEGIN
    RETURN query
    SELECT
        id,
        document_id,
        content,
        metadata,
        embedding,
        1 -(summaries.embedding <=> query_embedding) AS similarity
    FROM
        summaries
    WHERE 1 - (summaries.embedding <=> query_embedding) > match_threshold
    ORDER BY
        summaries.embedding <=> query_embedding
    LIMIT match_count;
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
    allowedDomains TEXT[] := ARRAY['%@theodo.fr', '%@theodo.com', '%@theodo.co.uk', '%@bam.tech', '%@padok.fr', '%@aleios.com', '%@sicara.com', '%@hokla.com', '%@sipios.com'];
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
        IF NOT NEW.models ? 'gpt-3.5-turbo-1106' THEN
            NEW.models := NEW.models || '["gpt-3.5-turbo"]'::jsonb;
        END IF;

        UPDATE user_settings
        SET 
            max_brains = 30,
            max_brain_size = 100000000,
            daily_chat_credit = 200,
            models = NEW.models
        WHERE user_id = NEW.user_id;
    END IF;

    RETURN NULL;  -- for AFTER triggers, the return value is ignored
END;
$function$
;

grant delete on table "public"."documents" to "anon";

grant insert on table "public"."documents" to "anon";

grant references on table "public"."documents" to "anon";

grant select on table "public"."documents" to "anon";

grant trigger on table "public"."documents" to "anon";

grant truncate on table "public"."documents" to "anon";

grant update on table "public"."documents" to "anon";

grant delete on table "public"."documents" to "authenticated";

grant insert on table "public"."documents" to "authenticated";

grant references on table "public"."documents" to "authenticated";

grant select on table "public"."documents" to "authenticated";

grant trigger on table "public"."documents" to "authenticated";

grant truncate on table "public"."documents" to "authenticated";

grant update on table "public"."documents" to "authenticated";

grant delete on table "public"."documents" to "service_role";

grant insert on table "public"."documents" to "service_role";

grant references on table "public"."documents" to "service_role";

grant select on table "public"."documents" to "service_role";

grant trigger on table "public"."documents" to "service_role";

grant truncate on table "public"."documents" to "service_role";

grant update on table "public"."documents" to "service_role";

CREATE TRIGGER update_max_brains_theodo_trigger AFTER INSERT ON public.user_settings FOR EACH ROW EXECUTE FUNCTION update_max_brains_theodo();


