-- Change vector ID type from BIGINT to UUID for langchain compatibility: https://github.com/hwchase17/langchain/commit/f773c217236ef07bea2203bc20d166569a0a0596
BEGIN;

-- Create a temporary mapping table
CREATE TEMP TABLE tmp_id_mapping (
    old_id BIGINT,
    new_id UUID
);

-- Generate new UUIDs for each row in vectors, store old and new IDs in mapping table
INSERT INTO tmp_id_mapping (old_id, new_id)
SELECT id, uuid_generate_v4() FROM vectors;

-- Create a new vectors table with the desired structure
CREATE TABLE vectors_new (
    id UUID PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);

-- Copy data from the old vectors table to the new one, replacing old IDs with new UUIDs
INSERT INTO vectors_new (id, content, metadata, embedding)
SELECT tmp_id_mapping.new_id, vectors.content, vectors.metadata, vectors.embedding
FROM vectors
JOIN tmp_id_mapping ON vectors.id = tmp_id_mapping.old_id;

-- Rename the old vectors table and the new one
ALTER TABLE vectors RENAME TO vectors_old;
ALTER TABLE vectors_new RENAME TO vectors;

-- Add new UUID columns in brains_vectors and summaries
ALTER TABLE brains_vectors ADD COLUMN new_vector_id UUID;
ALTER TABLE summaries ADD COLUMN new_document_id UUID;

-- Update the new columns in brains_vectors and summaries to match the new UUIDs
UPDATE brains_vectors
SET new_vector_id = tmp_id_mapping.new_id
FROM tmp_id_mapping
WHERE brains_vectors.vector_id = tmp_id_mapping.old_id;

UPDATE summaries
SET new_document_id = tmp_id_mapping.new_id
FROM tmp_id_mapping
WHERE summaries.document_id = tmp_id_mapping.old_id;

-- Drop old columns and rename new columns in brains_vectors and summaries
ALTER TABLE brains_vectors DROP COLUMN vector_id;
ALTER TABLE brains_vectors RENAME COLUMN new_vector_id TO vector_id;

ALTER TABLE summaries DROP COLUMN document_id;
ALTER TABLE summaries RENAME COLUMN new_document_id TO document_id;

-- Add foreign key constraints back to brains_vectors and summaries
ALTER TABLE brains_vectors ADD CONSTRAINT brains_vectors_vector_id_fkey FOREIGN KEY (vector_id) REFERENCES vectors (id);
ALTER TABLE summaries ADD CONSTRAINT summaries_document_id_fkey FOREIGN KEY (document_id) REFERENCES vectors (id);

-- Update the match_vectors function
DROP FUNCTION IF EXISTS match_vectors(VECTOR, INT, UUID);
CREATE FUNCTION match_vectors(query_embedding VECTOR(1536), match_count INT, p_brain_id UUID)
RETURNS TABLE(
    id UUID,
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

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '202307111517031_change_vectors_id_type'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '202307111517031_change_vectors_id_type'
);

COMMIT;
