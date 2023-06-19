from pydantic import BaseSettings


class BrainSettings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str
    supabase_url: str
    supabase_service_key: str
