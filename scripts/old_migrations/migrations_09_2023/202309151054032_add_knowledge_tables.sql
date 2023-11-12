BEGIN;

-- knowledge table
CREATE TABLE IF NOT EXISTS knowledge (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  file_name TEXT,
  url TEXT,
  brain_id UUID NOT NULL REFERENCES brains(brain_id),
  extension TEXT NOT NULL,
  CHECK ((file_name IS NOT NULL AND url IS NULL) OR (file_name IS NULL AND url IS NOT NULL))
);


-- knowledge_vectors table
CREATE TABLE IF NOT EXISTS knowledge_vectors (
  knowledge_id UUID NOT NULL REFERENCES knowledge(id),
  vector_id UUID NOT NULL REFERENCES vectors(id),
  embedding_model TEXT NOT NULL,
  PRIMARY KEY (knowledge_id, vector_id, embedding_model)
);

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '202309151054032_add_knowledge_tables'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '202309151054032_add_knowledge_tables'
);

COMMIT;
