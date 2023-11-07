-- Assuming the migration name is '20230906120000_create_notifications_table'

BEGIN;

-- Create notifications table if it doesn't exist
CREATE TABLE IF NOT EXISTS notifications (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  chat_id UUID REFERENCES chats(chat_id),
  message TEXT,
  action VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL
);

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20230906151400_add_notifications_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230906151400_add_notifications_table'
);

COMMIT;
