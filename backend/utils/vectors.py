from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from llm.brainpicking import BrainPicking, BrainSettings
from llm.summarization import llm_evaluate_summaries, llm_summerize
from logger import get_logger
from models.chats import ChatMessage
from models.settings import BrainSettings, CommonsDep
from pydantic import BaseModel

logger = get_logger(__name__)


class Neurons(BaseModel):
    commons: CommonsDep
    settings = BrainSettings()

    def create_vector(self, user_id, doc, user_openai_api_key=None):
        logger.info(f"Creating vector for document")
        logger.info(f"Document: {doc}")
        if user_openai_api_key:
            self.commons["documents_vector_store"]._embedding = OpenAIEmbeddings(
                openai_api_key=user_openai_api_key
            )
        try:
            sids = self.commons["documents_vector_store"].add_documents([doc])
            if sids and len(sids) > 0:
                self.commons["supabase"].table("vectors").update(
                    {"user_id": user_id}
                ).match({"id": sids[0]}).execute()
        except Exception as e:
            logger.error(f"Error creating vector for document {e}")

    def create_embedding(self, content):
        return self.commons["embeddings"].embed_query(content)

    def similarity_search(self, query, table="match_summaries", top_k=5, threshold=0.5):
        query_embedding = self.create_embedding(query)
        summaries = (
            self.commons["supabase"]
            .rpc(
                table,
                {
                    "query_embedding": query_embedding,
                    "match_count": top_k,
                    "match_threshold": threshold,
                },
            )
            .execute()
        )
        return summaries.data


def create_summary(commons: CommonsDep, document_id, content, metadata):
    logger.info(f"Summarizing document {content[:100]}")
    summary = llm_summerize(content)
    logger.info(f"Summary: {summary}")
    metadata["document_id"] = document_id
    summary_doc_with_metadata = Document(page_content=summary, metadata=metadata)
    sids = commons["summaries_vector_store"].add_documents([summary_doc_with_metadata])
    if sids and len(sids) > 0:
        commons["supabase"].table("summaries").update(
            {"document_id": document_id}
        ).match({"id": sids[0]}).execute()
