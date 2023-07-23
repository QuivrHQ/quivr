import os
from typing import Annotated

from fastapi import Depends, Request
from langchain.embeddings.openai import OpenAIEmbeddings
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
    resend_api_key: str = "null"
    resend_email_address: str = "brain@mail.quivr.app"


class LLMSettings(BaseSettings):
    private: bool = False
    model_path: str = "./local_models/ggml-gpt4all-j-v1.3-groovy.bin"


def common_dependencies() -> dict:
    settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none
    embeddings = OpenAIEmbeddings(
        openai_api_key=settings.openai_api_key
    )  # pyright: ignore reportPrivateUsage=none
    supabase_client: Client = create_client(
        settings.supabase_url, settings.supabase_service_key
    )
    documents_vector_store = SupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors"
    )
    summaries_vector_store = SupabaseVectorStore(
        supabase_client, embeddings, table_name="summaries"
    )

    return {
        "supabase": supabase_client,
        "embeddings": embeddings,
        "documents_vector_store": documents_vector_store,
        "summaries_vector_store": summaries_vector_store,
    }

async def brain_rate_limiting(request: Request) -> BrainRateLimiting:
    rate_limiting = BrainRateLimiting()
    if request.headers.get('Openai-Api-Key'):
        openai_limit = int(os.getenv(
                    "MAX_BRAIN_SIZE_WITH_KEY", 209715200
                ))
        return rate_limiting.copy(update=dict(max_brain_size=openai_limit))
    return rate_limiting

CommonsDep = Annotated[dict, Depends(common_dependencies)]
ProvideBrainRateLimit = Annotated[BrainRateLimiting, Depends(brain_rate_limiting)]

