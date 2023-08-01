BEGIN;

-- Create user_identity table if it doesn't exist
CREATE TABLE IF NOT EXISTS user_identity (
  user_id UUID PRIMARY KEY,
  openai_api_key VARCHAR(255)
);

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20230731172400_add_user_identity_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230731172400_add_user_identity_table'
);

COMMIT;
