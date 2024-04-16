alter table "public"."vectors" add column "fts" tsvector generated always as (to_tsvector('english'::regconfig, content)) stored;

CREATE INDEX vectors_fts_idx ON public.vectors USING gin (fts);

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.hybrid_match_vectors(query_text text, query_embedding vector, p_brain_id uuid, match_count integer, max_chunk_sum integer, full_text_weight double precision DEFAULT 1.0, semantic_weight double precision DEFAULT 1.0, rrf_k integer DEFAULT 50)
 RETURNS TABLE(id uuid, brain_id uuid, content text, metadata jsonb, embedding vector, similarity double precision, ft_rank double precision, rank_ix integer)
 LANGUAGE plpgsql
AS $function$
BEGIN
RETURN QUERY
WITH full_text AS (
    SELECT
        v.id,
        ts_rank_cd(v.fts, websearch_to_tsquery(query_text))::double precision AS ft_rank,
        row_number() OVER (ORDER BY ts_rank_cd(v.fts, websearch_to_tsquery(query_text)) DESC)::integer AS rank_ix,
        (v.metadata->>'chunk_size')::integer AS chunk_size
    FROM
        vectors v
    INNER JOIN
        brains_vectors bv ON v.id = bv.vector_id
    WHERE
        bv.brain_id = p_brain_id AND
        v.fts @@ websearch_to_tsquery(query_text)
    LIMIT LEAST(match_count, 30) * 2
), semantic AS (
    SELECT
        v.id,
        (1 - (v.embedding <#> query_embedding))::double precision AS semantic_similarity,
        row_number() OVER (ORDER BY (v.embedding <#> query_embedding))::integer AS rank_ix
    FROM
        vectors v
    INNER JOIN
        brains_vectors bv ON v.id = bv.vector_id
    WHERE
        bv.brain_id = p_brain_id
    LIMIT LEAST(match_count, 30) * 2
), combined AS (
    SELECT
        coalesce(ft.id, st.id) AS id,
        (coalesce(1.0 / (rrf_k + ft.rank_ix), 0)::double precision * full_text_weight + coalesce(1.0 / (rrf_k + st.rank_ix), 0)::double precision * semantic_weight)::double precision AS combined_score,
        ft.ft_rank,
        ft.rank_ix,
        ft.chunk_size
    FROM
        full_text ft
    FULL OUTER JOIN
        semantic st ON ft.id = st.id
), ranked_vectors AS (
    SELECT
        c.id,
        c.combined_score,
        sum(c.chunk_size) OVER (ORDER BY c.combined_score DESC, c.rank_ix)::integer AS running_total,
        c.ft_rank,
        c.rank_ix,
        c.chunk_size
    FROM
        combined c
)
SELECT
    v.id,
    bv.brain_id,
    v.content,
    v.metadata,
    v.embedding,
    c.combined_score::double precision AS similarity,
    c.ft_rank::double precision,
    c.rank_ix::integer
FROM
    ranked_vectors c
JOIN
    vectors v ON v.id = c.id
JOIN
    brains_vectors bv ON v.id = bv.vector_id
WHERE
    c.running_total <= max_chunk_sum
ORDER BY
    c.combined_score DESC, c.rank_ix
LIMIT
    LEAST(match_count, 30);
END;
$function$
;


