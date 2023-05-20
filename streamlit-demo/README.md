# Quivr

<p align="center">
<img src="../logo.png" alt="Quivr-logo" width="30%">
<p align="center">

<a href="https://discord.gg/HUpRgp2HG8">
  <img src="https://img.shields.io/badge/discord-join%20chat-blue.svg" alt="Join our Discord" height="40">
</a>

Quivr is your second brain in the cloud, designed to easily store and retrieve unstructured information. It's like Obsidian but powered by generative AI.

## Features

- **Store Anything**: Quivr can handle almost any type of data you throw at it. Text, images, code snippets, you name it.
- **Generative AI**: Quivr uses advanced AI to help you generate and retrieve information.
- **Fast and Efficient**: Designed with speed and efficiency in mind. Quivr makes sure you can access your data as quickly as possible.
- **Secure**: Your data is stored securely in the cloud and is always under your control.
- **Compatible Files**: 
  - **Text**
  - **Markdown**
  - **PDF**
  - **Audio**
  - **Video**
- **Open Source**: Quivr is open source and free to use.
## Demo


### Demo with GPT3.5
https://github.com/StanGirard/quivr/assets/19614572/80721777-2313-468f-b75e-09379f694653


### Demo with Claude 100k context
https://github.com/StanGirard/quivr/assets/5101573/9dba918c-9032-4c8d-9eea-94336d2c8bd4

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have the following installed before continuing:

- Python 3.10 or higher
- Pip
- Virtualenv

You'll also need a [Supabase](https://supabase.com/) account for:

- A new Supabase project
- Supabase Project API key
- Supabase Project URL

### Installing

- Clone the repository

```bash
git clone git@github.com:StanGirard/Quivr.git && cd Quivr
```

- Create a virtual environment

```bash
virtualenv venv
```

- Activate the virtual environment

```bash
source venv/bin/activate
```

- Install the dependencies

```bash
pip install -r requirements.txt
```

- Copy the streamlit secrets.toml example file

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

- Add your credentials to .streamlit/secrets.toml file

```toml
supabase_url = "SUPABASE_URL"
supabase_service_key = "SUPABASE_SERVICE_KEY"
openai_api_key = "OPENAI_API_KEY"
anthropic_api_key = "ANTHROPIC_API_KEY" # Optional
```

_Note that the `supabase_service_key` is found in your Supabase dashboard under Project Settings -> API. Use the `anon` `public` key found in the `Project API keys` section._

- Run the following migration scripts on the Supabase database via the web interface (SQL Editor -> `New query`)

```sql
-- Enable the pgvector extension to work with embedding vectors
       create extension vector;

       -- Create a table to store your documents
       create table documents (
       id bigserial primary key,
       content text, -- corresponds to Document.pageContent
       metadata jsonb, -- corresponds to Document.metadata
       embedding vector(1536) -- 1536 works for OpenAI embeddings, change if needed
       );

       CREATE FUNCTION match_documents(query_embedding vector(1536), match_count int)
           RETURNS TABLE(
               id bigint,
               content text,
               metadata jsonb,
               -- we return matched vectors to enable maximal marginal relevance searches
               embedding vector(1536),
               similarity float)
           LANGUAGE plpgsql
           AS $$
           # variable_conflict use_column
       BEGIN
           RETURN query
           SELECT
               id,
               content,
               metadata,
               embedding,
               1 -(documents.embedding <=> query_embedding) AS similarity
           FROM
               documents
           ORDER BY
               documents.embedding <=> query_embedding
           LIMIT match_count;
       END;
       $$;
```

and 

```sql
create table
  stats (
    -- A column called "time" with data type "timestamp"
    time timestamp,
    -- A column called "details" with data type "text"
    chat boolean,
    embedding boolean,
    details text,
    metadata jsonb,
    -- An "integer" primary key column called "id" that is generated always as identity
    id integer primary key generated always as identity
  );
```

- Run the app

```bash
streamlit run main.py
```

## Built With

* [NextJS](https://nextjs.org/) - The React framework used.
* [FastAPI](https://fastapi.tiangolo.com/) - The API framework used.
* [Supabase](https://supabase.io/) - The open source Firebase alternative.

## Contributing

Open a pull request and we'll review it as soon as possible.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=StanGirard/quivr&type=Date)](https://star-history.com/#StanGirard/quivr&Date)
