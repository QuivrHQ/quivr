from typing import Annotated

from fastapi import Depends
from langchain.embeddings.openai import OpenAIEmbeddings
from pydantic import BaseSettings
from supabase.client import Client, create_client
from vectorstore.supabase import SupabaseVectorStore


class BrainSettings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str
    supabase_url: str
    supabase_service_key: str


class LLMSettings(BaseSettings):
    private: bool = False
    model_path: str = "gpt2"
    model_n_ctx: int = 1000
    model_n_batch: int = 8


class CommonDependencies:
    def __init__(
        self,
        supabase: Client,
        embeddings: OpenAIEmbeddings,
        documents_vector_store: SupabaseVectorStore,
        summaries_vector_store: SupabaseVectorStore,
    ):
        self.supabase = supabase
        self.embeddings = embeddings
        self.documents_vector_store = documents_vector_store
        self.summaries_vector_store = summaries_vector_store


def common_dependencies() -> CommonDependencies:
    settings = BrainSettings(
        # type: ignore automatically loads .env file
    )

    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.openai_api_key,
        # type: ignore other parameters are optional
    )
    supabase_client: Client = create_client(
        settings.supabase_url, settings.supabase_service_key
    )
    documents_vector_store = SupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors"
    )
    summaries_vector_store = SupabaseVectorStore(
        supabase_client, embeddings, table_name="summaries"
    )

    return CommonDependencies(
        supabase_client,
        embeddings,
        documents_vector_store,
        summaries_vector_store,
    )


CommonsDep = Annotated[CommonDependencies, Depends(common_dependencies)]
