-- drop function if exists "public"."match_summaries"(query_embedding vector, match_count integer, match_threshold double precision);
DROP FUNCTION IF EXISTS public.match_summaries(vector, integer, double precision);

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20240103181925_cleanup'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20240103181925_cleanup'
);

COMMIT;