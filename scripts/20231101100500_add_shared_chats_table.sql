BEGIN;

-- Create shared_chats table if it doesn't exist
CREATE TABLE IF NOT EXISTS shared_chats (
  id UUID PRIMARY KEY,
  chat_id UUID default NULL
);

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20231101100500_add_shared_chats_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231101100500_add_shared_chats_table'
);

COMMIT;