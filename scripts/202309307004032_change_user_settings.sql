DO $$
BEGIN
    -- Check if the column max_requests_number exists
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name='user_settings' AND column_name='max_requests_number'
    ) THEN
        -- Rename the column
        ALTER TABLE user_settings RENAME COLUMN max_requests_number TO daily_chat_credit;
    END IF;
    
    -- Modify default values
    ALTER TABLE user_settings ALTER COLUMN daily_chat_credit SET DEFAULT 20;
    ALTER TABLE user_settings ALTER COLUMN max_brains SET DEFAULT 3;
END $$;

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '202309307004032_change_user_settings'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '202309307004032_change_user_settings'
);

COMMIT;

