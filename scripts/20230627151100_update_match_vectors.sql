-- Migration script
BEGIN;

-- Drop the old function if exists
DROP FUNCTION IF EXISTS match_vectors(VECTOR(1536), INT, TEXT);

-- Create the new function
CREATE OR REPLACE FUNCTION match_vectors(query_embedding VECTOR(1536), match_count INT, p_brain_id UUID)
RETURNS TABLE(
    id BIGINT,
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

INSERT INTO migrations (name) 
SELECT '20230627151100_update_match_vectors'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230627151100_update_match_vectors'
);

COMMIT;
