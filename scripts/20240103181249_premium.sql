-- alter table "public"."user_settings" add column "is_premium" boolean not null default false;
DO $$ BEGIN IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'user_settings'
    AND column_name = 'is_premium'
) THEN
    ALTER TABLE user_settings ADD COLUMN is_premium BOOLEAN NOT NULL DEFAULT false;
END IF;
END $$;

-- alter table "public"."user_settings" alter column "max_brain_size" set not null;
ALTER TABLE user_settings ALTER COLUMN max_brain_size SET NOT NULL;

-- alter table "public"."user_settings" alter column "max_brain_size" set data type bigint using "max_brain_size"::bigint;
ALTER TABLE user_settings ALTER COLUMN max_brain_size SET DATA TYPE BIGINT USING max_brain_size::BIGINT;

-- Insert migration record if it doesn't exist
INSERT INTO migrations (name)
SELECT '20240103181249_premium'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20240103181249_premium'
);

COMMIT;