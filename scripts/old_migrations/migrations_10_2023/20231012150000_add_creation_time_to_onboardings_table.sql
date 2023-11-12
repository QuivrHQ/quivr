-- Add creation_time column to 'onboardings' table if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'onboardings'
    AND column_name = 'creation_time'
  ) THEN
    ALTER TABLE onboardings ADD COLUMN creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
  END IF;
END
$$;

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20231012150000_add_creation_time_to_onboardings_table'
WHERE NOT EXISTS (
  SELECT 1 FROM migrations WHERE name = '20231012150000_add_creation_time_to_onboardings_table'
);

-- Commit the changes
COMMIT;
