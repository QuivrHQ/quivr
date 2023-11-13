BEGIN;

-- Change max_tokens type to INT
ALTER TABLE brains ALTER COLUMN max_tokens TYPE INT USING max_tokens::INT;

-- Add or rename the api_key column to openai_api_key
DO $$ 
BEGIN 
    BEGIN 
        -- Check if the api_key column exists
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'brains' AND column_name = 'api_key') THEN
            -- Rename the api_key column to openai_api_key
            ALTER TABLE brains RENAME COLUMN api_key TO openai_api_key;
        ELSE
            -- Create the openai_api_key column if it doesn't exist
            ALTER TABLE brains ADD COLUMN openai_api_key TEXT;
        END IF;
    END; 
END $$;

-- Add description column
ALTER TABLE brains ADD COLUMN description TEXT;

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '202307241530031_add_fields_to_brain'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '202307241530031_add_fields_to_brain'
);

COMMIT;
