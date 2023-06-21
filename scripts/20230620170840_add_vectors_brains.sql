-- Add a 'brain_id' column to 'vectors' table if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS(
      SELECT 1
      FROM   information_schema.columns 
      WHERE  table_name = 'vectors'
      AND    column_name = 'brain_id'
  ) THEN
    ALTER TABLE vectors ADD COLUMN brain_id UUID;
  END IF;
END
$$;

-- Copy corresponding 'user_id' from 'users' table to 'brain_id' in 'vectors' where 'email' matches
UPDATE vectors v 
SET brain_id = u.user_id 
FROM users u 
WHERE v.user_id = u.email;

-- Create a new entry in 'brains' table for each unique 'brain_id' in 'vectors', avoiding duplicates
INSERT INTO brains (brain_id, name, status, model, max_tokens, temperature)
SELECT brain_id, 'Default', 'active', 'gpt-3', '2048', 0.7 FROM vectors
ON CONFLICT (brain_id) DO NOTHING;

-- Create entries in 'brains_vectors' for all entries in 'vectors', avoiding duplicates
INSERT INTO brains_vectors (brain_id, vector_id)
SELECT brain_id, id FROM vectors
ON CONFLICT (brain_id, vector_id) DO NOTHING;

-- Add a 'default_brain' column to 'brains_users' table if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS(
      SELECT 1
      FROM   information_schema.columns 
      WHERE  table_name = 'brains_users'
      AND    column_name = 'default_brain'
  ) THEN
    ALTER TABLE brains_users ADD COLUMN default_brain BOOLEAN DEFAULT false;
  END IF;
END
$$;

-- Update 'default_brain' as 'true' for all current brains if it's NULL
UPDATE brains_users SET default_brain = true WHERE brain_id IN (SELECT brain_id FROM vectors) AND default_brain IS NULL;

-- Remove 'user_id' column if it exists
DO $$
BEGIN
  IF EXISTS(
      SELECT 1
      FROM   information_schema.columns 
      WHERE  table_name = 'vectors'
      AND    column_name = 'user_id'
  ) THEN
    ALTER TABLE vectors DROP COLUMN user_id;
  END IF;
END
$$;

-- Remove 'brain_id' column if it exists
DO $$
BEGIN
  IF EXISTS(
      SELECT 1
      FROM   information_schema.columns 
      WHERE  table_name = 'vectors'
      AND    column_name = 'brain_id'
  ) THEN
    ALTER TABLE vectors DROP COLUMN brain_id;
  END IF;
END
$$;
