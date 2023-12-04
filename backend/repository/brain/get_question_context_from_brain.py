from uuid import UUID

from logger import get_logger
from models.settings import get_embeddings, get_supabase_client
from vectorstore.supabase import CustomSupabaseVectorStore

logger = get_logger(__name__)


def get_question_context_from_brain(brain_id: UUID, question: str) -> str:
    # TODO: Move to AnswerGenerator service
    supabase_client = get_supabase_client()
    embeddings = get_embeddings()

    vector_store = CustomSupabaseVectorStore(
        supabase_client,
        embeddings,
        table_name="vectors",
        brain_id=str(brain_id),
    )
    documents = vector_store.similarity_search(question)
    ## I can't pass more than 2500 tokens to as return value in my array.  So i need to remove the docs after i reach 2000 tokens. A token equals 1.5 characters.  So 2000 tokens is 3000 characters.
    tokens = 0
    for doc in documents:
        tokens += len(doc.page_content) * 1.5
        if tokens > 3000:
            documents.remove(doc)
    logger.info("documents", documents)
    logger.info("tokens", tokens)
    logger.info("🔥🔥🔥🔥🔥🔥")

    # aggregate all the documents into one string
    return "\n".join([doc.page_content for doc in documents])
