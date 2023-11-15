DROP FUNCTION IF EXISTS public.get_user_id_by_user_email(text);

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20231114162700_drop_get_user_email_by_user_id'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231114162700_drop_get_user_email_by_user_id'
);

COMMIT;