CREATE OR REPLACE FUNCTION insert_secret(name text, secret text)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
begin
  return vault.create_secret(secret, name);
end;
$$;


create or replace function read_secret(secret_name text)
returns text
language plpgsql
security definer set search_path = public
as $$
declare
  secret text;
begin
  select decrypted_secret from vault.decrypted_secrets where name =
  secret_name into secret;
  return secret;
end;
$$;

create or replace function delete_secret(secret_name text)
returns text
language plpgsql
security definer set search_path = public
as $$
declare
 deleted_rows int;
begin
 delete from vault.decrypted_secrets where name = secret_name;
 get diagnostics deleted_rows = row_count;
 if deleted_rows = 0 then
   return false;
 else
   return true;
 end if;
end;
$$;

-- Insert a migration record if it doesn't exist
INSERT INTO migrations (name) 
SELECT '20231107104700_setup_vault'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231107104700_setup_vault'
);

-- Commit the changes
COMMIT;
