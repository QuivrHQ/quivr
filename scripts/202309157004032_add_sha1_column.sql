DO $$
BEGIN
    -- Check if file_sha1 column does not exist
    IF NOT EXISTS(SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'vectors' AND column_name = 'file_sha1') THEN
        -- Add the file_sha1 column
        ALTER TABLE public.vectors ADD COLUMN file_sha1 TEXT;

        -- Populate file_sha1 using metadata JSONB column
        UPDATE public.vectors SET file_sha1 = metadata->>'file_sha1';
    END IF;
END $$;


-- Update migrations table
INSERT INTO migrations (name) 
SELECT '202309157004032_add_sha1_column'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '202309157004032_add_sha1_column'
);

COMMIT;