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
^
-- Check if the server 'stripe_server' exists before creating it
DO $$
BEGIN
IF NOT EXISTS (SELECT 1 FROM pg_foreign_server WHERE srvname = 'stripe_server') THEN
CREATE SERVER stripe_server
FOREIGN DATA WRAPPER stripe_wrapper
OPTIONS (
api_key 'pk_test_51NtDTIJglvQxkJ1HgOBKicXBZ9Ug9pIhOZz3Lkask6q5JPZRoRW49nmwW6Q7wjWHJgc89HbruUP7GJ0d5DlQYOQ200MkvXpFnV' -- Replace with your Stripe API key
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


create schema if not exists extensions;

create table if not exists
  extensions.wrappers_fdw_stats ();

grant all on extensions.wrappers_fdw_stats to service_role;