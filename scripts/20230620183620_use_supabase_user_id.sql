-- Add the 'supabase_id' column to the 'users' table
ALTER TABLE users ADD COLUMN supabase_id UUID;

-- Update the 'supabase_id' column with the corresponding 'id' from 'auth.users'
UPDATE users
SET supabase_id = au.id
FROM auth.users au
WHERE users.email = au.email;

-- Update the 'chats' table
UPDATE chats
SET user_id = u.supabase_id
FROM users u
WHERE chats.user_id = u.user_id;

-- Update the 'brains_users' table
UPDATE brains_users
SET user_id = u.supabase_id
FROM users u
WHERE brains_users.user_id = u.user_id;

-- Update the 'api_keys' table
UPDATE api_keys
SET user_id = u.supabase_id
FROM users u
WHERE api_keys.user_id = u.user_id;

-- Drop the 'user_id' column from the 'users' table
ALTER TABLE users DROP COLUMN user_id;

-- Rename the 'supabase_id' column to 'user_id'
ALTER TABLE users RENAME COLUMN supabase_id TO user_id;
