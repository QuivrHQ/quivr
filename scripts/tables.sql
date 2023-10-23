-- Create users table
CREATE TABLE IF NOT EXISTS user_daily_usage(
    user_id UUID REFERENCES auth.users (id),
    email TEXT,
    date TEXT,
    daily_requests_count INT,
    PRIMARY KEY (user_id, date)
);

-- Create chats table
CREATE TABLE IF NOT EXISTS chats(
    chat_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES auth.users (id),
    creation_time TIMESTAMP DEFAULT current_timestamp,
    history JSONB,
    chat_name TEXT
);


-- Create vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create vectors table
CREATE TABLE IF NOT EXISTS vectors (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    content TEXT,
    file_sha1 TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);

-- Create function to match vectors
CREATE OR REPLACE FUNCTION match_vectors(query_embedding VECTOR(1536), match_count INT, p_brain_id UUID)
RETURNS TABLE(
    id UUID,
    brain_id UUID,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536),
    similarity FLOAT
) LANGUAGE plpgsql AS $$
#variable_conflict use_column
BEGIN
    RETURN QUERY
    SELECT
        vectors.id,
        brains_vectors.brain_id,
        vectors.content,
        vectors.metadata,
        vectors.embedding,
        1 - (vectors.embedding <=> query_embedding) AS similarity
    FROM
        vectors
    INNER JOIN
        brains_vectors ON vectors.id = brains_vectors.vector_id
    WHERE brains_vectors.brain_id = p_brain_id
    ORDER BY
        vectors.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create stats table
CREATE TABLE IF NOT EXISTS stats (
    time TIMESTAMP,
    chat BOOLEAN,
    embedding BOOLEAN,
    details TEXT,
    metadata JSONB,
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY
);

-- Create summaries table
CREATE TABLE IF NOT EXISTS summaries (
    id BIGSERIAL PRIMARY KEY,
    document_id UUID REFERENCES vectors(id),
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536)
);

-- Create function to match summaries
CREATE OR REPLACE FUNCTION match_summaries(query_embedding VECTOR(1536), match_count INT, match_threshold FLOAT)
RETURNS TABLE(
    id BIGINT,
    document_id UUID,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536),
    similarity FLOAT
) LANGUAGE plpgsql AS $$
#variable_conflict use_column
BEGIN
    RETURN QUERY
    SELECT
        id,
        document_id,
        content,
        metadata,
        embedding,
        1 - (summaries.embedding <=> query_embedding) AS similarity
    FROM
        summaries
    WHERE 1 - (summaries.embedding <=> query_embedding) > match_threshold
    ORDER BY
        summaries.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create api_keys table
CREATE TABLE IF NOT EXISTS api_keys(
    key_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users (id),
    api_key TEXT UNIQUE,
    creation_time TIMESTAMP DEFAULT current_timestamp,
    deleted_time TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

--- Create prompts table
CREATE TABLE IF NOT EXISTS prompts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    status VARCHAR(255) DEFAULT 'private'
);

--- Create brains table
CREATE TABLE IF NOT EXISTS brains (
  brain_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  status TEXT,
  description TEXT,
  model TEXT,
  max_tokens INT,
  temperature FLOAT,
  openai_api_key TEXT,
  prompt_id UUID REFERENCES prompts(id),
  last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Create chat_history table
CREATE TABLE IF NOT EXISTS chat_history (
    message_id UUID DEFAULT uuid_generate_v4(),
    chat_id UUID REFERENCES chats(chat_id),
    user_message TEXT,
    assistant TEXT,
    message_time TIMESTAMP DEFAULT current_timestamp,
    PRIMARY KEY (chat_id, message_id),
    prompt_id UUID REFERENCES prompts(id),
    brain_id UUID REFERENCES brains(brain_id)
);

-- Create notification table

CREATE TABLE IF NOT EXISTS notifications (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  chat_id UUID REFERENCES chats(chat_id),
  message TEXT,
  action VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL
);


-- Create brains X users table
CREATE TABLE IF NOT EXISTS brains_users (
  brain_id UUID,
  user_id UUID,
  rights VARCHAR(255),
  default_brain BOOLEAN DEFAULT false,
  PRIMARY KEY (brain_id, user_id),
  FOREIGN KEY (user_id) REFERENCES auth.users (id),
  FOREIGN KEY (brain_id) REFERENCES brains (brain_id)
);

-- Create brains X vectors table
CREATE TABLE IF NOT EXISTS brains_vectors (
  brain_id UUID,
  vector_id UUID,
  file_sha1 TEXT,
  PRIMARY KEY (brain_id, vector_id),
  FOREIGN KEY (vector_id) REFERENCES vectors (id),
  FOREIGN KEY (brain_id) REFERENCES brains (brain_id)
);

-- Create brains X vectors table
CREATE TABLE IF NOT EXISTS brain_subscription_invitations (
  brain_id UUID,
  email VARCHAR(255),
  rights VARCHAR(255),
  PRIMARY KEY (brain_id, email),
  FOREIGN KEY (brain_id) REFERENCES brains (brain_id)
);

--- Create user_identity table
CREATE TABLE IF NOT EXISTS user_identity (
  user_id UUID PRIMARY KEY,
  openai_api_key VARCHAR(255)
);


CREATE OR REPLACE FUNCTION public.get_user_email_by_user_id(user_id uuid)
RETURNS TABLE (email text)
SECURITY definer
AS $$
BEGIN
  RETURN QUERY SELECT au.email::text FROM auth.users au WHERE au.id = user_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION public.get_user_id_by_user_email(user_email text)
RETURNS TABLE (user_id uuid)
SECURITY DEFINER
AS $$
BEGIN
  RETURN QUERY SELECT au.id::uuid FROM auth.users au WHERE au.email = user_email;
END;
$$ LANGUAGE plpgsql;



CREATE TABLE IF NOT EXISTS migrations (
  name VARCHAR(255)  PRIMARY KEY,
  executed_at TIMESTAMPTZ DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS user_settings (
  user_id UUID PRIMARY KEY,
  models JSONB DEFAULT '["gpt-3.5-turbo","huggingface/mistralai/Mistral-7B-Instruct-v0.1"]'::jsonb,
  daily_chat_credit INT DEFAULT 20,
  max_brains INT DEFAULT 3,
  max_brain_size INT DEFAULT 10000000
);

-- knowledge table
CREATE TABLE IF NOT EXISTS knowledge (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  file_name TEXT,
  url TEXT,
  brain_id UUID NOT NULL REFERENCES brains(brain_id),
  extension TEXT NOT NULL,
  CHECK ((file_name IS NOT NULL AND url IS NULL) OR (file_name IS NULL AND url IS NOT NULL))
);


-- knowledge_vectors table
CREATE TABLE IF NOT EXISTS knowledge_vectors (
  knowledge_id UUID NOT NULL REFERENCES knowledge(id),
  vector_id UUID NOT NULL REFERENCES vectors(id),
  embedding_model TEXT NOT NULL,
  PRIMARY KEY (knowledge_id, vector_id, embedding_model)
);

-- Create the function to add user_id to the onboardings table
CREATE OR REPLACE FUNCTION public.create_user_onboarding() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.onboardings (user_id)
    VALUES (NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY definer;

-- Revoke all on function handle_new_user_onboarding() from PUBLIC;
REVOKE ALL ON FUNCTION create_user_onboarding() FROM PUBLIC;

-- Drop the trigger if it exists
DROP TRIGGER IF EXISTS create_user_onboarding_trigger ON auth.users;

-- Create the trigger on the insert into the auth.users table
CREATE TRIGGER create_user_onboarding_trigger
AFTER INSERT ON auth.users
FOR EACH ROW
EXECUTE FUNCTION public.create_user_onboarding();

-- Create the onboarding table
CREATE TABLE IF NOT EXISTS onboardings (
  user_id UUID NOT NULL REFERENCES auth.users (id),
  onboarding_a BOOLEAN NOT NULL DEFAULT true,
  onboarding_b1 BOOLEAN NOT NULL DEFAULT true,
  onboarding_b2 BOOLEAN NOT NULL DEFAULT true,
  onboarding_b3 BOOLEAN NOT NULL DEFAULT true,
  creation_time TIMESTAMP DEFAULT current_timestamp,
  PRIMARY KEY (user_id)
);


-- Stripe settings --
-- Create extension 'wrappers' if it doesn't exist
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

-- Check if the server 'stripe_server' exists before creating it
DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_foreign_server WHERE srvname = 'stripe_server') THEN
    CREATE SERVER stripe_server
      FOREIGN DATA WRAPPER stripe_wrapper
      OPTIONS (
        api_key 'your_stripe_api_key'  -- Replace with your Stripe API key
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

-- Create table 'users' if it doesn't exist
CREATE TABLE IF NOT EXISTS public.users (
  id uuid REFERENCES auth.users NOT NULL PRIMARY KEY,
  email text
);

-- Create or replace function 'public.handle_new_user' 
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if the trigger 'on_auth_user_created' exists before creating it
DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'on_auth_user_created') THEN
    CREATE TRIGGER on_auth_user_created
      AFTER INSERT ON auth.users
      FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
  END IF;
END $$;

insert into
  storage.buckets (id, name)
values
  ('quivr', 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_0" ON storage.objects FOR INSERT TO anon WITH CHECK (bucket_id = 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_1" ON storage.objects FOR SELECT TO anon USING (bucket_id = 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_2" ON storage.objects FOR UPDATE TO anon USING (bucket_id = 'quivr');

CREATE POLICY "Access Quivr Storage 1jccrwz_3" ON storage.objects FOR DELETE TO anon USING (bucket_id = 'quivr');

INSERT INTO migrations (name) 
SELECT '20231023160000_copy_auth_users_to_public_users'
WHERE NOT EXISTS (
    SELECT 1 FROM migrations WHERE name = '20231023160000_copy_auth_users_to_public_users'
);


