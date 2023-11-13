CREATE OR REPLACE FUNCTION public.get_user_id_by_user_email(user_email text)
RETURNS TABLE (user_id uuid)
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY SELECT au.id::uuid FROM auth.users au WHERE au.email = user_email;
END;
$$ LANGUAGE plpgsql;

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20230717173000_add_get_user_id_by_user_email'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230717173000_add_get_user_id_by_user_email'
);

COMMIT;
