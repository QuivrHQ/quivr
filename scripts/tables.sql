-- Create users table
CREATE TABLE IF NOT EXISTS users(
    user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT,
    date TEXT,
    requests_count INT
);

-- Create chats table
CREATE TABLE IF NOT EXISTS chats(
    chat_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    creation_time TIMESTAMP DEFAULT current_timestamp,
    history JSONB,
    chat_name TEXT
);

-- Create vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create vectors table
CREATE TABLE IF NOT EXISTS vectors (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);

-- Create function to match vectors
CREATE OR REPLACE FUNCTION match_vectors(query_embedding VECTOR(1536), match_count INT, p_user_id TEXT)
RETURNS TABLE(
    id BIGINT,
    user_id TEXT,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536),
    similarity FLOAT
) LANGUAGE plpgsql AS $$
#variable_conflict use_column
BEGIN
    RETURN QUERY
    SELECT
        id,
        user_id,
        content,
        metadata,
        embedding,
        1 - (vectors.embedding <=> query_embedding) AS similarity
    FROM
        vectors
    WHERE vectors.user_id = p_user_id
    ORDER BY
        vectors.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create stats table
CREATE TABLE IF NOT EXISTS stats (
    time TIMESTAMP,
    chat BOOLEAN,
    embedding BOOLEAN,
    details TEXT,
    metadata JSONB,
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY
);

-- Create summaries table
CREATE TABLE IF NOT EXISTS summaries (
    id BIGSERIAL PRIMARY KEY,
    document_id BIGINT REFERENCES vectors(id),
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);

-- Create function to match summaries
CREATE OR REPLACE FUNCTION match_summaries(query_embedding VECTOR(1536), match_count INT, match_threshold FLOAT)
RETURNS TABLE(
    id BIGINT,
    document_id BIGINT,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536),
    similarity FLOAT
) LANGUAGE plpgsql AS $$
#variable_conflict use_column
BEGIN
    RETURN QUERY
    SELECT
        id,
        document_id,
        content,
        metadata,
        embedding,
        1 - (summaries.embedding <=> query_embedding) AS similarity
    FROM
        summaries
    WHERE 1 - (summaries.embedding <=> query_embedding) > match_threshold
    ORDER BY
        summaries.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create api_keys table
CREATE TABLE IF NOT EXISTS api_keys(
    key_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    api_key TEXT UNIQUE,
    creation_time TIMESTAMP DEFAULT current_timestamp,
    deleted_time TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

