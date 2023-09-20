-- Assuming you have a table named "prompts" with columns: "title", "content", "status"

CREATE TABLE IF NOT EXISTS user_settings (
  user_id UUID PRIMARY KEY,
  models JSONB DEFAULT '["gpt-3.5-turbo"]'::jsonb,
  max_requests_number INT DEFAULT 50,
  max_brains INT DEFAULT 5,
  max_brain_size INT DEFAULT 10000000
);


-- Update migrations table
INSERT INTO migrations (name) 
SELECT '202309127004032_add_user_limits'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '202309127004032_add_user_limits'
);

COMMIT;
