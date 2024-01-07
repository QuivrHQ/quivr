-- create foreign table public.subscriptions (
--   id text,
--   customer text,
--   currency text,
--   current_period_start timestamp,
--   current_period_end timestamp,
--   attrs jsonb
-- ) server stripe_server options (object 'subscriptions', rowid_column 'id');
CREATE FOREIGN TABLE IF NOT EXISTS public.subscriptions (
  id text,
  customer text,
  currency text,
  current_period_start timestamp,
  current_period_end timestamp,
  attrs jsonb
) SERVER stripe_server OPTIONS (object 'subscriptions', rowid_column 'id');

-- create foreign table public.products (
--   id text,
--   name text,
--   active bool,
--   default_price text,
--   description text,
--   created timestamp,
--   updated timestamp,
--   attrs jsonb
-- ) server stripe_server options (object 'products', rowid_column 'id');
CREATE FOREIGN TABLE IF NOT EXISTS public.products (
  id text,
  name text,
  active bool,
  default_price text,
  description text,
  created timestamp,
  updated timestamp,
  attrs jsonb
) SERVER stripe_server OPTIONS (object 'products', rowid_column 'id');

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name)
SELECT '20240103193921_stripe_customers'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20240103193921_stripe_customers'
);

COMMIT;