
-- Create the function to add user_id to the onboardings table
CREATE OR REPLACE FUNCTION public.create_user_onboarding() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.onboardings (user_id)
    VALUES (NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY definer;

-- Revoke all on function handle_new_user_onboarding() from PUBLIC;
REVOKE ALL ON FUNCTION create_user_onboarding() FROM PUBLIC;

-- Drop the trigger if it exists
DROP TRIGGER IF EXISTS create_user_onboarding_trigger ON auth.users;

-- Create the trigger on the insert into the auth.users table
CREATE TRIGGER create_user_onboarding_trigger
AFTER INSERT ON auth.users
FOR EACH ROW
EXECUTE FUNCTION public.create_user_onboarding();

-- Update migrations table
INSERT INTO migrations (name)
SELECT '20231010120000_add_create_user_onboarding_function'
WHERE NOT EXISTS (
    SELECT 1
    FROM migrations
    WHERE name = '20231010120000_add_create_user_onboarding_function'
);
