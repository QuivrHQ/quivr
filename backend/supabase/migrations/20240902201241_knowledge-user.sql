alter table "public"."knowledge" add column "user_id" uuid;
alter table "public"."knowledge" add constraint "public_knowledge_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE not valid;
alter table "public"."knowledge" validate constraint "public_knowledge_user_id_fkey";

-- alter table
ALTER TABLE "public"."knowledge"
DROP CONSTRAINT "unique_file_sha1";

ALTER TABLE "public"."knowledge"
ADD CONSTRAINT "unique_file_sha1_user_id" UNIQUE ("file_sha1", "user_id");
