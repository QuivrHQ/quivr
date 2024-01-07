BEGIN;

-- Function to check if column exists in a table
DO $$ 
BEGIN
    -- Check if email column doesn't exist, then add it
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'email') THEN
        ALTER TABLE users ADD COLUMN email TEXT;
    END IF;
    
    -- Copy user_id to email column only if user_id column exists
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'user_id') THEN
        UPDATE users SET email = user_id;
    END IF;
    
    -- Check if user_id column exists, then drop it
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'user_id') THEN
        ALTER TABLE users DROP COLUMN user_id;
    END IF;

    -- Check if new user_id column doesn't exist, then add it
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'user_id') THEN
        ALTER TABLE users ADD COLUMN user_id UUID DEFAULT gen_random_uuid();
        ALTER TABLE users ADD PRIMARY KEY (user_id);
    END IF;
    
EXCEPTION WHEN others THEN
    -- Exception block to catch errors
    RAISE NOTICE 'An error occurred during migration.';
END;
$$ LANGUAGE plpgsql;

INSERT INTO migrations (name) 
SELECT '20230606131110_add_uuid_user_id'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230606131110_add_uuid_user_id'
);

COMMIT;

