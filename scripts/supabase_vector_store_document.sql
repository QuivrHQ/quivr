create extension vector;

-- Create a table to store your documents
create table if not exists documents (
id bigserial primary key,
content text, -- corresponds to Document.pageContent
metadata jsonb, -- corresponds to Document.metadata
embedding vector(1536) -- 1536 works for OpenAI embeddings, change if needed
);

CREATE FUNCTION match_documents(query_embedding vector(1536), match_count int)
    RETURNS TABLE(
        id bigint,
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
        content,
        metadata,
        embedding,
        1 -(documents.embedding <=> query_embedding) AS similarity
    FROM
        documents
    ORDER BY
        documents.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;