from concurrent.futures import ThreadPoolExecutor
from typing import List
from uuid import UUID

from logger import get_logger
from models.settings import get_documents_vector_store, get_embeddings, get_supabase_db
from pydantic import BaseModel

logger = get_logger(__name__)


# TODO: Create interface for embeddings and implement it for Supabase and OpenAI (current Quivr)
class Neurons(BaseModel):
    def create_vector(self, docs):
        documents_vector_store = get_documents_vector_store()

        try:
            sids = documents_vector_store.add_documents(docs)
            if sids and len(sids) > 0:
                return sids

        except Exception as e:
            logger.error(f"Error creating vector for document {e}")

    def create_embedding(self, content):
        embeddings = get_embeddings()
        return embeddings.embed_query(content)


def error_callback(exception):
    print("An exception occurred:", exception)


def process_batch(batch_ids: List[str]):
    supabase_db = get_supabase_db()

    try:
        if len(batch_ids) == 1:
            return (supabase_db.get_vectors_by_batch(UUID(batch_ids[0]))).data
        else:
            return (supabase_db.get_vectors_in_batch(batch_ids)).data
    except Exception as e:
        logger.error("Error retrieving batched vectors", e)


# TODO: move to Knowledge class
def get_unique_files_from_vector_ids(vectors_ids):
    # Move into Vectors class
    """
    Retrieve unique user data vectors.
    """

    # constants
    BATCH_SIZE = 5

    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(vectors_ids), BATCH_SIZE):
            batch_ids = vectors_ids[i : i + BATCH_SIZE]
            future = executor.submit(process_batch, batch_ids)
            futures.append(future)

        # Retrieve the results
        vectors_responses = [future.result() for future in futures]

    documents = [item for sublist in vectors_responses for item in sublist]
    unique_files = [dict(t) for t in set(tuple(d.items()) for d in documents)]
    return unique_files
