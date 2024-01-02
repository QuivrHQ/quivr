DO $$
BEGIN

-- Check if 'composite' already exists in the enum
IF NOT EXISTS (
    SELECT 1 FROM pg_enum 
    WHERE enumlabel = 'composite' 
    AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'brain_type_enum')
) THEN
    -- Add 'composite' to the enum
    ALTER TYPE brain_type_enum ADD VALUE 'composite';
END IF;

-- Table for storing the relationship between brains for composite brains
CREATE TABLE IF NOT EXISTS composite_brain_connections (
  composite_brain_id UUID NOT NULL REFERENCES brains(brain_id),
  connected_brain_id UUID NOT NULL REFERENCES brains(brain_id),
  PRIMARY KEY (composite_brain_id, connected_brain_id),
  CHECK (composite_brain_id != connected_brain_id)
);

END $$;


-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20231205163000_new_table_composite_brain_connections'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231205163000_new_table_composite_brain_connections'
);

COMMIT;
