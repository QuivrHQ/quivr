-- alter table "public"."user_settings" add column "API_ACCESS" boolean not null default false;
ALTER TABLE user_settings ADD COLUMN API_ACCESS BOOLEAN NOT NULL DEFAULT false;

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name)
SELECT '20240103194255_api'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20240103194255_api'
);

COMMIT;
