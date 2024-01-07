insert into
  storage.buckets (id, name)
values
  ('quivr', 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_0" ON storage.objects FOR INSERT TO anon WITH CHECK (bucket_id = 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_1" ON storage.objects FOR SELECT TO anon USING (bucket_id = 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_2" ON storage.objects FOR UPDATE TO anon USING (bucket_id = 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_3" ON storage.objects FOR DELETE TO anon USING (bucket_id = 'quivr');

-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20230913110420_add_storage_bucket'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20230913110420_add_storage_bucket'
);

COMMIT;
