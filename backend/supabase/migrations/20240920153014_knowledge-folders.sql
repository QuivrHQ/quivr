ALTER USER postgres
SET idle_session_timeout = '3min';
ALTER USER postgres
SET idle_in_transaction_session_timeout = '3min';
-- Drop previous contraint
alter table "public"."knowledge" drop constraint "unique_file_sha1_user_id";
alter table "public"."knowledge"
add column "is_folder" boolean default false;
-- Update the knowledge to backfill knowledge to is_folder = false
UPDATE "public"."knowledge"
SET is_folder = false;
-- Add parent_id -> folder
alter table "public"."knowledge"
add column "parent_id" uuid;
alter table "public"."knowledge"
add constraint "public_knowledge_parent_id_fkey" FOREIGN KEY (parent_id) REFERENCES knowledge(id) ON DELETE CASCADE;
-- Add constraint must be folder for parent_id
CREATE FUNCTION is_parent_folder(folder_id uuid) RETURNS boolean AS $$ BEGIN RETURN (
    SELECT k.is_folder
    FROM public.knowledge k
    WHERE k.id = folder_id
);
END;
$$ LANGUAGE plpgsql;
ALTER TABLE public.knowledge
ADD CONSTRAINT check_parent_is_folder CHECK (
        parent_id IS NULL
        OR is_parent_folder(parent_id)
    );
-- Index on parent_id
CREATE INDEX knowledge_parent_id_idx ON public.knowledge USING btree (parent_id);
