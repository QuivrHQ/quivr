from uuid import UUID

from models.settings import get_embeddings, get_supabase_client
from vectorstore.supabase import CustomSupabaseVectorStore


def get_question_context_from_brain(brain_id: UUID, question: str) -> str:
    supabase_client = get_supabase_client()
    embeddings = get_embeddings()

    vector_store = CustomSupabaseVectorStore(
        supabase_client,
        embeddings,
        table_name="vectors",
        brain_id=str(brain_id),
    )
    documents = vector_store.similarity_search(question)

    # aggregate all the documents into one string
    return "\n".join([doc.page_content for doc in documents])
