BEGIN;

-- Create user_identity table if it doesn't exist
CREATE TABLE IF NOT EXISTS prompts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    status VARCHAR(255) DEFAULT 'private'
);


-- Insert migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20230701180101_add_prompts_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230701180101_add_prompts_table'
);

COMMIT;
