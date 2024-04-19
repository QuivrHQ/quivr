from uuid import UUID

from attr import dataclass
from logger import get_logger
from models.settings import get_embeddings, get_supabase_client
from modules.upload.service.generate_file_signed_url import generate_file_signed_url
from vectorstore.supabase import CustomSupabaseVectorStore

logger = get_logger(__name__)


@dataclass
class DocumentAnswer:
    file_name: str
    file_sha1: str
    file_size: int
    file_url: str = ""
    file_id: str = ""
    file_similarity: float = 0.0


def get_question_context_from_brain(brain_id: UUID, question: str) -> str:
    """Finds the best brain to answer the question based on the question's meaning.

    Args:
        brain_id (UUID): Id of the brain to search in
        question (str): Question to search for in the vector store

    Returns:
        str: _descripton_
    """
    # TODO: Move to AnswerGenerator service
    supabase_client = get_supabase_client()
    embeddings = get_embeddings()

    vector_store = CustomSupabaseVectorStore(
        supabase_client,
        embeddings,
        table_name="vectors",
        brain_id=str(brain_id),
        number_docs=20,
    )
    documents = vector_store.similarity_search(question, k=20, threshold=0.8)

    answers = []
    file_sha1s = []
    for document in documents:
        if document.metadata["file_sha1"] not in file_sha1s:
            file_sha1s.append(document.metadata["file_sha1"])
            file_path_in_storage = f"{brain_id}/{document.metadata['file_name']}"
            answers.append(
                DocumentAnswer(
                    file_name=document.metadata["file_name"],
                    file_sha1=document.metadata["file_sha1"],
                    file_size=document.metadata["file_size"],
                    file_id=document.metadata["id"],
                    file_similarity=document.metadata["similarity"],
                    file_url=generate_file_signed_url(file_path_in_storage).get(
                        "signedURL", ""
                    ),
                ),
            )

    return answers
