-- Auth users to public users -- 

INSERT INTO public.users (id, email)
SELECT id, email
FROM auth.users
ON CONFLICT (id) DO NOTHING;

INSERT INTO migrations (name) 
SELECT '20231023160000_copy_auth_users_to_public_users'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231023160000_copy_auth_users_to_public_users'
);

COMMIT;
