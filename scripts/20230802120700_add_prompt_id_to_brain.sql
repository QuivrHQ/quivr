BEGIN;

-- Check if prompt_id column exists
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'brains' AND column_name = 'prompt_id') THEN
        -- Add prompt_id column and reference the table prompts' id column
        ALTER TABLE brains ADD COLUMN prompt_id UUID REFERENCES prompts(id);
    END IF;
END $$;

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20230802120700_add_prompt_id_to_brain'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230802120700_add_prompt_id_to_brain'
);

COMMIT;
