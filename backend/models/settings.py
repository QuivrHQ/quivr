from typing import Annotated, Any, Dict, List, Tuple, Union

from fastapi import Depends
from langchain.embeddings.openai import OpenAIEmbeddings
from pydantic import BaseSettings
from supabase import Client, create_client
from vectorstore.supabase import SupabaseVectorStore


class BrainSettings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str
    supabase_url: str
    supabase_service_key: str

class LLMSettings(BaseSettings):
    private: bool
    model_path: str
    model_n_ctx: int
    model_n_batch: int

def common_dependencies() -> dict:
    settings = BrainSettings()
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    supabase_client: Client = create_client(settings.supabase_url, settings.supabase_service_key)
    documents_vector_store = SupabaseVectorStore(
    supabase_client, embeddings, table_name="vectors")
    summaries_vector_store = SupabaseVectorStore(
        supabase_client, embeddings, table_name="summaries")
    
    return {
        "supabase": supabase_client,
        "embeddings": embeddings,
        "documents_vector_store": documents_vector_store,
        "summaries_vector_store": summaries_vector_store
    }

CommonsDep = Annotated[dict, Depends(common_dependencies)]