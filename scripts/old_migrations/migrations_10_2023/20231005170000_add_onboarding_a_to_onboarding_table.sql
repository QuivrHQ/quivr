-- Check if onboarding_a column exists
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'onboardings' AND column_name = 'onboarding_a') THEN
        ALTER TABLE onboardings ADD COLUMN onboarding_a BOOLEAN NOT NULL DEFAULT true; 
    END IF;
END $$;

COMMIT;


-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20231005170000_add_onboarding_a_to_onboarding_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231005170000_add_onboarding_a_to_onboarding_table'
);