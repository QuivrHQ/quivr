BEGIN;

-- Add the file_sha1 column if it doesn't exist
ALTER TABLE IF EXISTS brains_vectors
ADD COLUMN IF NOT EXISTS file_sha1 TEXT;

-- Update the file_sha1 column with values from vectors.metadata
UPDATE brains_vectors
SET file_sha1 = subquery.file_sha1
FROM (
    SELECT vectors.id, vectors.metadata->>'file_sha1' AS file_sha1
    FROM vectors
) AS subquery
WHERE brains_vectors.vector_id = subquery.id
AND (brains_vectors.file_sha1 IS NULL OR brains_vectors.file_sha1 = '');


INSERT INTO migrations (name) 
SELECT '20230629143400_add_file_sha1_brains_vectors'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230629143400_add_file_sha1_brains_vectors'
);

COMMIT;
