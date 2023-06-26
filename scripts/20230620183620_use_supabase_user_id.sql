

-- Add the 'supabase_id' column to the 'users' table
ALTER TABLE users ADD COLUMN supabase_id UUID;

-- Update the 'supabase_id' column with the corresponding 'id' from 'auth.users'
UPDATE users
SET supabase_id = au.id
FROM auth.users au
WHERE users.email = au.email;

-- Create a copy of old users table for safety
CREATE TABLE users_old AS TABLE users;

-- Drop the old primary key
ALTER TABLE users DROP CONSTRAINT users_pkey1;

-- Get the name of your constraint key
-- SELECT 
--     conname AS constraint_name,
--     conrelid::regclass AS table_name,
--     contype AS constraint_type
-- FROM 
--     pg_constraint 
-- WHERE 
--     conrelid::regclass = 'users'::regclass;

ALTER TABLE users RENAME COLUMN user_id TO old_user_id;
ALTER TABLE users RENAME COLUMN supabase_id TO user_id;

--- Create a new primary key with user_id and date
ALTER TABLE users ADD PRIMARY KEY (user_id, date);

-- Delete duplicate rows from the 'users' table
-- DELETE FROM users
-- WHERE ctid NOT IN (
--     SELECT min(ctid)
--     FROM users
--     GROUP BY old_user_id
-- );

-- Update the 'chats' table
ALTER TABLE chats DROP CONSTRAINT chats_user_id_fkey;
UPDATE chats
SET user_id = u.user_id
FROM users u
WHERE chats.user_id = u.old_user_id;
ALTER TABLE chats ADD CONSTRAINT chats_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id);



-- Update the 'brains_users' table
--- Delete users with user_id not in supabase auth
DELETE FROM brains_users
WHERE NOT EXISTS (
    SELECT 1 
    FROM auth.users 
    WHERE brains_users.user_id = auth.users.id
);

ALTER TABLE brains_users DROP CONSTRAINT brains_users_user_id_fkey;
UPDATE brains_users
SET user_id = u.user_id
FROM users u
WHERE brains_users.user_id = u.old_user_id;
ALTER TABLE brains_users ADD CONSTRAINT brains_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id);


-- Update the 'api_keys' table
ALTER TABLE api_keys DROP CONSTRAINT api_keys_user_id_fkey;
UPDATE api_keys
SET user_id = u.user_id
FROM users u
WHERE api_keys.user_id = u.old_user_id;
ALTER TABLE api_keys ADD CONSTRAINT api_keys_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id);


-- -- Drop the 'user_id' column from the 'users' table
-- ALTER TABLE users DROP COLUMN old_user_id;
