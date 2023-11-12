-- Add the 'supabase_id' column to the 'users' table if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS(
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'users'
    AND column_name = 'supabase_id'
  ) THEN
    ALTER TABLE users ADD COLUMN supabase_id UUID;
  END IF;
END
$$;

-- Update the 'supabase_id' column with the corresponding 'id' from 'auth.users'
-- Fails if there's no matching email in auth.users
UPDATE users
SET supabase_id = au.id
FROM auth.users au
WHERE users.email = au.email;

-- Create a copy of old users table for safety
-- Fails if 'users_old' table already exists
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_name = 'users_old'
  ) THEN
    CREATE TABLE users_old AS TABLE users;
  END IF;
END
$$;

-- Drop the old primary key if it exists
DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'users_pkey'
  ) THEN
    ALTER TABLE users DROP CONSTRAINT users_pkey CASCADE;
  END IF;
END
$$;

-- Rename columns if not already renamed
DO $$
BEGIN
  IF EXISTS(
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'users'
    AND column_name = 'user_id'
  ) AND NOT EXISTS(
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'users'
    AND column_name = 'old_user_id'
  ) THEN
    ALTER TABLE users RENAME COLUMN user_id TO old_user_id;
    ALTER TABLE users RENAME COLUMN supabase_id TO user_id;
  END IF;
END
$$;

-- Create a new primary key with user_id and date if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM pg_constraint
    WHERE conname = 'users_pkey'
  ) THEN
    ALTER TABLE users ADD PRIMARY KEY (user_id, date);
  END IF;
END
$$;

-- Update the 'chats' table
-- Drop old foreign key constraint if it exists
DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.table_constraints
    WHERE constraint_name = 'chats_user_id_fkey'
  ) THEN
    ALTER TABLE chats DROP CONSTRAINT chats_user_id_fkey;
  END IF;
END
$$;

-- Update user_id in chats
-- Fails if there's no matching old_user_id in users
UPDATE chats
SET user_id = u.user_id::uuid
FROM users u
WHERE chats.user_id::uuid = u.old_user_id::uuid;

-- Add new foreign key constraint if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.table_constraints
    WHERE constraint_name = 'chats_user_id_fkey'
  ) THEN
    ALTER TABLE chats ADD CONSTRAINT chats_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id);
  END IF;
END
$$;

-- Update the 'brains_users' table

-- Add a new 'new_user_id' column to the 'brains_users' table
ALTER TABLE brains_users ADD COLUMN new_user_id UUID;

-- Update 'new_user_id' in the 'brains_users' table based on the 'email' in the 'users' table
UPDATE brains_users bu
SET new_user_id = u.user_id
FROM users u
WHERE bu.user_id = u.email;

-- Once you are sure that 'new_user_id' has been correctly populated, drop the old 'user_id' column
ALTER TABLE brains_users DROP COLUMN user_id;

-- Rename 'new_user_id' column to 'user_id'
ALTER TABLE brains_users RENAME COLUMN new_user_id TO user_id;


-- Delete users with user_id not in supabase auth
DELETE FROM brains_users
WHERE NOT EXISTS (
    SELECT 1 
    FROM auth.users 
    WHERE brains_users.user_id = auth.users.id
);

-- Drop old foreign key constraint if it exists
DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.table_constraints
    WHERE constraint_name = 'brains_users_user_id_fkey'
  ) THEN
    ALTER TABLE brains_users DROP CONSTRAINT brains_users_user_id_fkey;
  END IF;
END
$$;

-- Update user_id in brains_users
-- Fails if there's no matching old_user_id in users
UPDATE brains_users
SET user_id = u.user_id::uuid
FROM users u
WHERE brains_users.user_id::uuid = u.old_user_id::uuid;

-- Add new foreign key constraints if they don't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.table_constraints
    WHERE constraint_name = 'brains_users_user_id_fkey'
  ) THEN
    ALTER TABLE brains_users ADD CONSTRAINT brains_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id);
    --ALTER TABLE brains_users ADD CONSTRAINT brains_users_brain_id_fkey FOREIGN KEY (brain_id) REFERENCES brains (brain_id);
  END IF;
END
$$;

-- Update the 'api_keys' table
-- Drop old foreign key constraint if it exists
DO $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM information_schema.table_constraints
    WHERE constraint_name = 'api_keys_user_id_fkey'
  ) THEN
    ALTER TABLE api_keys DROP CONSTRAINT api_keys_user_id_fkey;
  END IF;
END
$$;

-- Update user_id in api_keys
-- Fails if there's no matching old_user_id in users
UPDATE api_keys
SET user_id = u.user_id::uuid
FROM users u
WHERE api_keys.user_id::uuid = u.old_user_id::uuid;

-- Add new foreign key constraint if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.table_constraints
    WHERE constraint_name = 'api_keys_user_id_fkey'
  ) THEN
    ALTER TABLE api_keys ADD CONSTRAINT api_keys_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id);
  END IF;
END
$$;

-- Optionally Drop the 'old_user_id' column from the 'users' table
-- Uncomment if you are sure that it is no longer needed.
--ALTER TABLE users DROP COLUMN old_user_id;

INSERT INTO migrations (name) 
SELECT '20230627151100_update_match_vectors'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230627151100_update_match_vectors'
);