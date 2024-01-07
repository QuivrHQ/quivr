-- Check if the ENUM type 'brain_type' already exists
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'brain_type_enum') THEN
    -- Create the ENUM type 'brain_type' if it doesn't exist
    CREATE TYPE brain_type_enum AS ENUM ('doc', 'api');
  END IF;
END $$;

-- Add a column 'brain_type' to the 'brains' table using the 'brain_type' ENUM type
BEGIN;

-- Add a column 'brain_type' to the 'brains' table as the 'brain_type' ENUM type with a default value 'doc'
DO $$ 
BEGIN 
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'brains'
        AND column_name = 'brain_type'
    ) THEN
        ALTER TABLE brains ADD COLUMN brain_type brain_type_enum DEFAULT 'doc';
    END IF;
END $$;

-- Insert a migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20231106110000_add_field_brain_type_to_brain_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231106110000_add_field_brain_type_to_brain_table'
);

-- Commit the changes
COMMIT;
