BEGIN;

-- Create a new column for email and copy the current user_id to it
ALTER TABLE users ADD COLUMN email text;
UPDATE users SET email = user_id;

-- Drop the current user_id column
ALTER TABLE users DROP COLUMN user_id;

-- Create a new UUID user_id column and set it as the primary key
ALTER TABLE users ADD COLUMN user_id UUID DEFAULT gen_random_uuid() PRIMARY KEY;

COMMIT;
