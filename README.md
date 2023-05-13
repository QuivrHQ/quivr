# Quiver

<p align="center">
<img src="./logo.png" alt="quiver-logo" width="30%">
<p align="center">

Quiver is your second brain in the cloud, designed to easily store and retrieve unstructured information. It's like Obsidian but powered by generative AI.

## Features

- **Store Anything**: Quiver can handle almost any type of data you throw at it. Text, images, code snippets, you name it.
- **Generative AI**: Quiver uses advanced AI to help you generate and retrieve information.
- **Fast and Efficient**: Designed with speed and efficiency in mind. Quiver makes sure you can access your data as quickly as possible.
- **Secure**: Your data is stored securely in the cloud and is always under your control.
- **Compatible Files**: 
  - **Text**
  - **Markdown**
  - **PDF**
  - **Audio**
  - **Video**
- **Open Source**: Quiver is open source and free to use.
## Demo



https://github.com/StanGirard/quiver/assets/19614572/a3cddc6a-ca28-44ad-9ede-3122fa918b51



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.

- Python 3.10 or higher
- Pip
- Virtualenv
- Supabase account
- Supabase API key
- Supabase URL

### Installing

- Clone the repository

```bash
git clone git@github.com:StanGirard/quiver.git & cd quiver
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
```

- Run the migration script on the Supabase database via the web interface

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

- Run the app

```bash
streamlit run main.py
```

## Built With

* [Python](https://www.python.org/) - The programming language used.
* [Streamlit](https://streamlit.io/) - The web framework used.
* [Supabase](https://supabase.io/) - The open source Firebase alternative.

## Contributing

Open a pull request and we'll review it as soon as possible.

