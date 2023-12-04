from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from logger import get_logger
from models.databases.supabase.supabase import SupabaseDB
from pydantic import BaseSettings
from supabase.client import Client, create_client
from vectorstore.supabase import SupabaseVectorStore

logger = get_logger(__name__)


class BrainRateLimiting(BaseSettings):
    max_brain_per_user: int = 5


class BrainSettings(BaseSettings):
    openai_api_key: str
    supabase_url: str
    supabase_service_key: str
    resend_api_key: str = "null"
    resend_email_address: str = "brain@mail.quivr.app"
    ollama_api_base_url: str = None


class ResendSettings(BaseSettings):
    resend_api_key: str = "null"


def get_supabase_client() -> Client:
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none
    supabase_client: Client = create_client(
        settings.supabase_url, settings.supabase_service_key
    )
    return supabase_client


def get_supabase_db() -> SupabaseDB:
    supabase_client = get_supabase_client()
    return SupabaseDB(supabase_client)


def get_embeddings():
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none
    if settings.ollama_api_base_url:
        embeddings = OllamaEmbeddings(
            base_url=settings.ollama_api_base_url,
        )  # pyright: ignore reportPrivateUsage=none
    else:
        embeddings = OpenAIEmbeddings()  # pyright: ignore reportPrivateUsage=none
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
