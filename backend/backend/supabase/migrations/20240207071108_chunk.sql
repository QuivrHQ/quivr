alter table "public"."brains_vectors" drop constraint "brains_vectors_vector_id_fkey";

drop function if exists "public"."match_vectors"(query_embedding vector, match_count integer, p_brain_id uuid);

CREATE INDEX vectors_metadata_idx ON public.vectors USING gin (metadata);

alter table "public"."brains_vectors" add constraint "brains_vectors_vector_id_fkey" FOREIGN KEY (vector_id) REFERENCES vectors(id) ON UPDATE CASCADE ON DELETE CASCADE not valid;

alter table "public"."brains_vectors" validate constraint "brains_vectors_vector_id_fkey";

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.match_vectors(query_embedding vector, p_brain_id uuid, max_chunk_sum integer)
 RETURNS TABLE(id uuid, brain_id uuid, content text, metadata jsonb, embedding vector, similarity double precision)
 LANGUAGE plpgsql
AS $function$
BEGIN
    RETURN QUERY
    WITH ranked_vectors AS (
        SELECT
            v.id AS vector_id, -- Explicitly qualified
            bv.brain_id AS vector_brain_id, -- Explicitly qualified and aliased
            v.content AS vector_content, -- Explicitly qualified and aliased
            v.metadata AS vector_metadata, -- Explicitly qualified and aliased
            v.embedding AS vector_embedding, -- Explicitly qualified and aliased
            1 - (v.embedding <=> query_embedding) AS calculated_similarity, -- Calculated and aliased
            (v.metadata->>'chunk_size')::integer AS chunk_size -- Explicitly qualified
        FROM
            vectors v
        INNER JOIN
            brains_vectors bv ON v.id = bv.vector_id
        WHERE
            bv.brain_id = p_brain_id
        ORDER BY
            calculated_similarity -- Aliased similarity
    ), filtered_vectors AS (
        SELECT
            vector_id,
            vector_brain_id,
            vector_content,
            vector_metadata,
            vector_embedding,
            calculated_similarity,
            chunk_size,
            sum(chunk_size) OVER (ORDER BY calculated_similarity) AS running_total
        FROM ranked_vectors
    )
    SELECT
        vector_id AS id,
        vector_brain_id AS brain_id,
        vector_content AS content,
        vector_metadata AS metadata,
        vector_embedding AS embedding,
        calculated_similarity AS similarity
    FROM filtered_vectors
    WHERE running_total <= max_chunk_sum;
END;
$function$
;


