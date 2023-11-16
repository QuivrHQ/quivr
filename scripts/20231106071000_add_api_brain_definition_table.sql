-- Create the new table with 6 columns
CREATE TABLE IF NOT EXISTS api_brain_definition (
    brain_id UUID REFERENCES brains(brain_id),
    method VARCHAR(255) CHECK (method IN ('GET', 'POST', 'PUT', 'DELETE')),
    url VARCHAR(255),
    params JSON,
    search_params JSON,
    secrets JSON
);

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20231106071000_add_api_brain_definition_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231106071000_add_api_brain_definition_table'
);

COMMIT;