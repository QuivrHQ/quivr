BEGIN;

-- Create brain_subscription_invitations table if it doesn't exist
CREATE TABLE IF NOT EXISTS brain_subscription_invitations (
  brain_id UUID,
  email VARCHAR(255),
  rights VARCHAR(255),
  PRIMARY KEY (brain_id, email),
  FOREIGN KEY (brain_id) REFERENCES Brains (brain_id)
);

INSERT INTO migrations (name) 
SELECT '202307111517030_add_subscription_invitations_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '202307111517030_add_subscription_invitations_table'
);

COMMIT;
