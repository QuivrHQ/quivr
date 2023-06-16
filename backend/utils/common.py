import os
from typing import Annotated

from fastapi import Depends
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from logger import get_logger

from supabase import Client, create_client

logger = get_logger(__name__)

openai_api_key = os.environ.get("OPENAI_API_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
supabase_client: Client = create_client(supabase_url, supabase_key)
documents_vector_store = SupabaseVectorStore(
    supabase_client, embeddings, table_name="vectors")
summaries_vector_store = SupabaseVectorStore(
    supabase_client, embeddings, table_name="summaries")


def common_dependencies():
    return {
        "supabase": supabase_client,
        "embeddings": embeddings,
        "documents_vector_store": documents_vector_store,
        "summaries_vector_store": summaries_vector_store
    }


CommonsDep = Annotated[dict, Depends(common_dependencies)]