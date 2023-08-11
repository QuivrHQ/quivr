from langchain.embeddings.openai import OpenAIEmbeddings
from models.databases.supabase.supabase import SupabaseDB
from pydantic import BaseSettings
from supabase.client import Client, create_client
from vectorstore.supabase import SupabaseVectorStore


class BrainRateLimiting(BaseSettings):
    max_brain_size: int = 52428800
    max_brain_per_user: int = 5


class BrainSettings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str
    supabase_url: str
    supabase_service_key: str
    pg_database_url: str = "not implemented"
    resend_api_key: str = "null"
    resend_email_address: str = "brain@mail.quivr.app"
    openai_api_base: str = "https://api.openai.com/v1"
    openai_api_type: str = "open_ai"
    azure_gpt_deployment_id : str = None   # pyright: ignore reportPrivateUsage=none
    azure_embedding_deployment_id : str = None  # pyright: ignore reportPrivateUsage=none
    azure_api_version : str = "2023-07-01-preview"

class LLMSettings(BaseSettings):
    private: bool = False
    model_path: str = "./local_models/ggml-gpt4all-j-v1.3-groovy.bin"


def get_supabase_client() -> Client:
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none
    supabase_client: Client = create_client(
        settings.supabase_url, settings.supabase_service_key
    )
    return supabase_client


def get_supabase_db() -> SupabaseDB:
    supabase_client = get_supabase_client()
    return SupabaseDB(supabase_client)


def get_embeddings() -> OpenAIEmbeddings:
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none

    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.openai_api_key,
        openai_api_base=settings.openai_api_base,
        deployment=settings.azure_embedding_deployment_id,
        openai_api_type=settings.azure_api_type,
        openai_api_version=settings.azure_api_version,
    )  # pyright: ignore reportPrivateUsage=none
    return embeddings


def get_documents_vector_store() -> SupabaseVectorStore:
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none
    embeddings = get_embeddings()
    supabase_client: Client = create_client(
        settings.supabase_url, settings.supabase_service_key
    )
    documents_vector_store = SupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors"
    )
    return documents_vector_store
