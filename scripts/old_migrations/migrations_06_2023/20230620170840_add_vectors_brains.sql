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


-- Copy corresponding 'user_id' from 'users' table to 'brain_id' in 'vectors' where 'email' matches only if 'brain_id' is NULL or not equal to 'user_id'
UPDATE vectors v 
SET brain_id = u.user_id 
FROM users u 
WHERE v.user_id = u.email AND (v.brain_id IS NULL OR v.brain_id != u.user_id);

-- Delete rows in 'vectors' where 'brain_id' is NULL
DELETE FROM vectors
WHERE brain_id IS NULL;

-- Create a new entry in 'brains' table for each unique 'brain_id' in 'vectors', avoiding duplicates
INSERT INTO brains (brain_id, name, status, model, max_tokens, temperature)
SELECT brain_id, 'Default', 'public', 'gpt-3', '2048', 0.7 FROM vectors
ON CONFLICT (brain_id) DO NOTHING;

-- Create entries in 'brains_vectors' for all entries in 'vectors', avoiding duplicates
INSERT INTO brains_vectors (brain_id, vector_id)
SELECT brain_id, id FROM vectors
ON CONFLICT (brain_id, vector_id) DO NOTHING;


ALTER TABLE brains_users DROP CONSTRAINT brains_users_user_id_fkey;

ALTER TABLE brains_users ALTER COLUMN user_id TYPE TEXT USING user_id::TEXT;



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

INSERT INTO brains_users (brain_id, user_id, default_brain)
SELECT brain_id, user_id, true FROM vectors
ON CONFLICT (brain_id, user_id) DO NOTHING;


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


INSERT INTO migrations (name) 
SELECT '20230620170840_add_vectors_brains'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230620170840_add_vectors_brains'
);