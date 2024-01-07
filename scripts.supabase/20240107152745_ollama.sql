ALTER TABLE public.vectors ALTER COLUMN "embedding" SET NOT NULL;

ALTER TABLE public.vectors ALTER COLUMN "embedding" SET DATA TYPE vector USING "embedding"::vector;

ALTER TABLE public.summaries ALTER COLUMN "embedding" SET NOT NULL;

ALTER TABLE public.summaries ALTER COLUMN "embedding" SET DATA TYPE vector USING "embedding"::vector;

-- Create function to match vectors
CREATE OR REPLACE FUNCTION match_vectors(query_embedding VECTOR, match_count INT, p_brain_id UUID)
RETURNS TABLE(
    id UUID,
    brain_id UUID,
    content TEXT,
    metadata JSONB,
    embedding VECTOR,
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

INSERT INTO public.models ("name", "price", "max_input", "max_output") VALUES
    ('ollama/llama2', 1, 2000, 1000);

-- Update migrations table
INSERT INTO migrations (name)
SELECT '20240107152745_ollama'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20240107152745_ollama'
);

COMMIT;
