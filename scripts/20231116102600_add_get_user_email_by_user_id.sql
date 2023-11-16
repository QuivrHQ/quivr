CREATE OR REPLACE FUNCTION public.get_user_email_by_user_id(user_id uuid)
RETURNS TABLE (email text)
SECURITY definer
AS $$
BEGIN
  RETURN QUERY SELECT au.email::text FROM auth.users au WHERE au.id = user_id;
END;
$$ LANGUAGE plpgsql;

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20231116102600_add_get_user_email_by_user_id'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231116102600_add_get_user_email_by_user_id'
);

COMMIT;
