-- Create extension 'wrappers' if it doesn't exist
CREATE EXTENSION IF NOT EXISTS wrappers;

-- Create foreign data wrapper 'stripe_wrapper' if it doesn't exist
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 
    FROM information_schema.foreign_data_wrappers 
    WHERE foreign_data_wrapper_name = 'stripe_wrapper'
  ) THEN
    CREATE FOREIGN DATA WRAPPER stripe_wrapper
      HANDLER stripe_fdw_handler;
  END IF;
END $$;

-- Check if the server 'stripe_server' exists before creating it
DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_foreign_server WHERE srvname = 'stripe_server') THEN
    CREATE SERVER stripe_server
      FOREIGN DATA WRAPPER stripe_wrapper
      OPTIONS (
        api_key 'your_stripe_api_key'  -- Replace with your Stripe API key
      );
  END IF;
END $$;

-- Create foreign table 'public.customers' if it doesn't exist
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_name = 'customers' 
  ) THEN
    CREATE FOREIGN TABLE public.customers (
      id text,
      email text,
      name text,
      description text,
      created timestamp,
      attrs jsonb
    )
    SERVER stripe_server
    OPTIONS (
      OBJECT 'customers',
      ROWID_COLUMN 'id'
    );
  END IF;
END $$;

-- Create table 'users' if it doesn't exist
CREATE TABLE IF NOT EXISTS public.users (
  id uuid REFERENCES auth.users NOT NULL PRIMARY KEY,
  email text
);

-- Create or replace function 'public.handle_new_user' 
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if the trigger 'on_auth_user_created' exists before creating it
DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'on_auth_user_created') THEN
    CREATE TRIGGER on_auth_user_created
      AFTER INSERT ON auth.users
      FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
  END IF;
END $$;

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20231023140000_add_stripe_wrapper'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231023140000_add_stripe_wrapper'
);

COMMIT;
