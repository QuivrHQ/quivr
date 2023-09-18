DO $$
BEGIN
    -- Check if file_sha1 column does not exist
    alter table public.brains
    add column retriever_algorithm text;
END $$;


-- Update migrations table
INSERT INTO migrations (name) 
SELECT '202309189504032_add_retrieval_algorithm'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '202309189504032_add_retrieval_algorithm'
);

COMMIT;