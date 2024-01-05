DO $$
BEGIN
    -- Check if the messages table does not exist
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_tables 
                   WHERE schemaname = 'public' AND tablename  = 'messages') THEN
        
        -- Create the table if it does not exist
        CREATE TABLE public.messages (
            message_id uuid NOT NULL DEFAULT gen_random_uuid(),
            brain_id uuid NOT NULL,
            user_id uuid NOT NULL,
            content text NOT NULL,
            created_at timestamp without time zone NOT NULL DEFAULT current_timestamp,
            CONSTRAINT messages_pkey PRIMARY KEY (message_id),
            CONSTRAINT messages_brain_id_fkey FOREIGN KEY (brain_id) REFERENCES public.brains (brain_id),
            CONSTRAINT messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id)
        ) TABLESPACE pg_default;

        RAISE NOTICE 'Created table public.messages';
    ELSE
        RAISE NOTICE 'Table public.messages already exists';
    END IF;
END $$;


-- Update migrations table
INSERT INTO migrations (name) 
SELECT '20231209003200_new_message_table'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231209003200_new_message_table'
);

COMMIT;
