DO $$
BEGIN
    -- Add 'name' column if it does not exist
    IF NOT EXISTS (SELECT FROM pg_attribute WHERE attrelid = 'api_keys'::regclass AND attname = 'name') THEN
        ALTER TABLE api_keys ADD COLUMN name TEXT DEFAULT 'API_KEY';
    END IF;

    -- Add 'days' column if it does not exist
    IF NOT EXISTS (SELECT FROM pg_attribute WHERE attrelid = 'api_keys'::regclass AND attname = 'days') THEN
        ALTER TABLE api_keys ADD COLUMN days INT DEFAULT 30;
    END IF;

    -- Add 'only_chat' column if it does not exist
    IF NOT EXISTS (SELECT FROM pg_attribute WHERE attrelid = 'api_keys'::regclass AND attname = 'only_chat') THEN
        ALTER TABLE api_keys ADD COLUMN only_chat BOOLEAN DEFAULT false;
    END IF;

    -- Optionally, update default values for existing rows if necessary
    -- UPDATE api_keys SET name = 'API_KEY' WHERE name IS NULL;
    -- UPDATE api_keys SET days = 30 WHERE days IS NULL;
    -- UPDATE api_keys SET only_chat = false WHERE only_chat IS NULL;

END $$;


-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20231203173900_new_api_key_format'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231203173900_new_api_key_format'
);

COMMIT;
