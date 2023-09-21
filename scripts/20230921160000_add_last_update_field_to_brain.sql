-- Add last_update column to 'brains' table if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'brains'
    AND column_name = 'last_update'
  ) THEN
    ALTER TABLE brains ADD COLUMN last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
  END IF;
END
$$;

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20230921160000_add_last_update_field_to_brain'
WHERE NOT EXISTS (
  SELECT 1 FROM migrations WHERE name = '20230921160000_add_last_update_field_to_brain'
);

-- Commit the changes
COMMIT;
