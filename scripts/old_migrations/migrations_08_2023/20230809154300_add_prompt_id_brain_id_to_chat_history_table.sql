BEGIN;

-- Check if brain_id column exists in chat_history table
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'chat_history' AND column_name = 'brain_id') THEN
        -- Add brain_id column
        ALTER TABLE chat_history ADD COLUMN brain_id UUID REFERENCES brains(brain_id);
    END IF;
END $$;

-- Check if prompt_id column exists in chat_history table
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'chat_history' AND column_name = 'prompt_id') THEN
        -- Add prompt_id column
        ALTER TABLE chat_history ADD COLUMN prompt_id UUID REFERENCES prompts(id);
    END IF;
END $$;

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20230809154300_add_prompt_id_brain_id_to_chat_history_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230809154300_add_prompt_id_brain_id_to_chat_history_table'
);

COMMIT;
