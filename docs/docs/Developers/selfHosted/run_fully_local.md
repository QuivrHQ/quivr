---
sidebar_position: 2
title: Run Quivr locally with Ollama
---

# Using Quivr fully locally with Ollama

## Headers

The following is a guide to set up everything for using Quivr locally:

##### Table of Contents

- [Database](#database)
- [Embeddings](#embeddings)
- [LLM for inference](#llm)

The guide was put together in collaboration with members of the Quivr Discord, **Using Quivr fully locally** thread. That is a good place to discuss it. https://discord.com/invite/HUpRgp2HG8

<a name="database"/>

## Local Supabase

Instead of relying on a remote Supabase instance, we have to set it up locally. Follow the instructions on https://supabase.com/docs/guides/self-hosting/docker.

Troubleshooting:

- If the Quivr backend container cannot reach Supabase on port 8000, change the Quivr backend container to use the host network.
- If email service does not work, add a user using the supabase web ui, and check "Auto Confirm User?".
  - http://localhost:8000/project/default/auth/users

<a name="embeddings"/>

## Ollama

Ollama is a tool that allows you to run LLMs locally. We are using it to run Llama2, MistralAI and others locally. 

### Install Ollama

Install Ollama from their [website](https://ollama.ai/).

Then run the following command to run Ollama in the background:

```bash
ollama run llama2
```

### Update Quivr to use Ollama

In order to have Quivr use Ollama we need to update the  tables in Supabase to support the embedding format that Ollama uses. Ollama uses by default llama 2 that produces 4096 dimensional embeddings while OpenAI API produces 1536 dimensional embeddings. 


Go to supabase and delete your table vectors and create a new table vectors with the following schema:

```sql
CREATE TABLE IF NOT EXISTS vectors (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    content TEXT,
    file_sha1 TEXT,
    metadata JSONB,
    embedding VECTOR(4096)
);
``` 

Then run the following command to update the table:

```sql
CREATE OR REPLACE FUNCTION match_vectors(query_embedding VECTOR(4096), match_count INT, p_brain_id UUID)
RETURNS TABLE(
    id UUID,
    brain_id UUID,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(4096),
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
``` 

This will update the match_vectors function to use the new embedding format.


## Add Ollama Model to Quivr

Now that you have your model running locally, you need to add it to Quivr.

In order to allow the user to choose between the OpenAI API and Ollama, we need to add a new model to the Quivr backend.

Go to supabase and in the table `user_settings` either add by default or to your user the following value to the `models` column:

```json
[
  "gpt-3.5-turbo-1106",
  "ollama/llama2"
]
```

This will add the Ollama model to the list of models that the user can choose from.

By adding this as default, it means that all new users will have this model by default. If you want to add it to your user only, you can add it to the `models` column in the `user_settings` table. In order for the change to take effect if you put as default your need to drop the entire table with the following command:

```sql
DROP TABLE user_settings;
```


## Env Variables


In order to have Quivr use Ollama we need to update the env variables.

Go to `backend/.env` and add the following env variables:

```bash
OLLAMA_API_BASE_URL=http://host.docker.internal:11434
```

Then go to the Quivr and you are good to go.