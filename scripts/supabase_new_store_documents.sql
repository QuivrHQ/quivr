create extension if not exists vector;

-- Create a table to store your documents
create table if not exists vectors (
id bigserial primary key,
user_id text, -- new column added here
content text, -- corresponds to Document.pageContent
metadata jsonb, -- corresponds to Document.metadata
embedding vector(1536) -- 1536 works for OpenAI embeddings, change if needed
);

CREATE OR REPLACE FUNCTION match_vectors(query_embedding vector(1536), match_count int, p_user_id text) -- user_id changed to p_user_id here
    RETURNS TABLE(
        id bigint,
        user_id text, -- new column added here
        content text,
        metadata jsonb,
        -- we return matched vectors to enable maximal marginal relevance searches
        embedding vector(1536),
        similarity float)
    LANGUAGE plpgsql
    AS $$
    # variable_conflict use_column
BEGIN
    RETURN query
    SELECT
        id,
        user_id, -- new column added here
        content,
        metadata,
        embedding,
        1 -(vectors.embedding <=> query_embedding) AS similarity
    FROM
        vectors
    WHERE vectors.user_id = p_user_id -- filter changed here
    ORDER BY
        vectors.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
