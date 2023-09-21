from celery import shared_task
from models.brains import Brain
from models.settings import get_supabase_db
from repository.files.upload_file import DocumentSerializable
from utils.vectors import Neurons


@shared_task
def create_embedding_for_document(
    brain_id, doc_with_metadata, user_openai_api_key, file_sha1
):
    neurons = Neurons()
    doc = DocumentSerializable.from_json(doc_with_metadata)
    created_vector = neurons.create_vector(doc, user_openai_api_key)
    database = get_supabase_db()
    database.set_file_sha_from_metadata(file_sha1)

    created_vector_id = created_vector[0]  # pyright: ignore reportPrivateUsage=none

    brain = Brain(id=brain_id)  # pyright: ignore
    brain.create_brain_vector(created_vector_id, file_sha1)
