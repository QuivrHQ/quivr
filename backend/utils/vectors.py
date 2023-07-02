from langchain.embeddings.openai import OpenAIEmbeddings
from llm.brainpicking import BrainSettings
from logger import get_logger  # type: ignore
from models.settings import BrainSettings, CommonsDep
from pydantic import BaseModel
from typing import Optional, Any

logger = get_logger(__name__)


class Neurons(BaseModel):
    commons: CommonsDep
    settings = BrainSettings(
        # type: ignore automatically loads .env file
    )

    def create_vector(self, doc: Any, user_openai_api_key: Optional[str] = None):
        logger.info(f"Creating vector for document")
        logger.info(f"Document: {doc}")
        if user_openai_api_key:
            self.commons.documents_vector_store.__setattr__(
                "_embedding",
                OpenAIEmbeddings(
                    openai_api_key=user_openai_api_key
                    # type: ignore
                ),
            )

        try:
            sids = self.commons.documents_vector_store.add_documents([doc])
            if sids and len(sids) > 0:
                return sids

        except Exception as e:
            logger.error(f"Error creating vector for document {e}")

    def create_embedding(self, content: str):
        return self.commons.embeddings.embed_query(content)

    def similarity_search(
        self,
        query: str,
        table: str = "match_summaries",
        top_k: int = 5,
        threshold: float = 0.5,
    ):
        query_embedding = self.create_embedding(query)
        summaries = self.commons.supabase.rpc(
            table,
            {
                "query_embedding": query_embedding,
                "match_count": top_k,
                "match_threshold": threshold,
            },
        ).execute()
        return summaries.data
