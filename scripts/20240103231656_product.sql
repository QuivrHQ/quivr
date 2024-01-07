-- alter table "public"."product_to_features" alter column "models" set not null;
ALTER TABLE public.product_to_features ALTER COLUMN models SET NOT NULL;

-- Update migration record if it doesn't exist
INSERT INTO migrations (name)
SELECT '20240103231656_product'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20240103231656_product'
);

COMMIT;

