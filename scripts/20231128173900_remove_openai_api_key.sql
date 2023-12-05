DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'brains' AND column_name = 'openai_api_key'
    ) THEN
        -- Column exists, so drop it
        ALTER TABLE brains
        DROP COLUMN openai_api_key;
    END IF;
END $$;


-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20231128173900_remove_openai_api_key'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231128173900_remove_openai_api_key'
);

COMMIT;
