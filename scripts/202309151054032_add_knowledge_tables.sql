BEGIN;

-- knowledge table
CREATE TABLE IF NOT EXISTS knowledge (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  file_id UUID REFERENCES storage.objects(id),
  url VARCHAR,
  content_sha1 CHAR(40) NOT NULL,
  user_id UUID NOT NULL REFERENCES auth.users(id),
  knowledge_name VARCHAR NOT NULL,
  extension VARCHAR NOT NULL,
  summary TEXT,
  CHECK ((file_id IS NOT NULL AND url IS NULL) OR (file_id IS NULL AND url IS NOT NULL))
);

-- brain_knowledge table
CREATE TABLE IF NOT EXISTS brain_knowledge (
  brain_id UUID NOT NULL REFERENCES brains(brain_id),
  knowledge_id UUID NOT NULL REFERENCES knowledge(id),
  PRIMARY KEY (brain_id, knowledge_id)
);

-- knowledge_vectors table
CREATE TABLE IF NOT EXISTS knowledge_vectors (
  knowledge_id UUID NOT NULL REFERENCES knowledge(id),
  vector_id UUID NOT NULL REFERENCES vectors(id),
  embedding_model VARCHAR NOT NULL,
  PRIMARY KEY (knowledge_id, vector_id, embedding_model)
);

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '202309151054032_add_knowledge_tables'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '202309151054032_add_knowledge_tables'
);

COMMIT;
