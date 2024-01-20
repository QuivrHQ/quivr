drop function if exists "public"."match_documents"(query_embedding vector, match_count integer);

alter table "public"."chat_history" add column "metadata" jsonb;


