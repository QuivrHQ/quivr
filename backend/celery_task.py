from celery import shared_task
from models.brains import Brain
from models.settings import get_supabase_db
from packages.embeddings.vectors import Neurons
from repository.files.upload_file import DocumentSerializable


@shared_task
def create_embedding_for_document(brain_id, doc_with_metadata, file_sha1):
    neurons = Neurons()
    doc = DocumentSerializable.from_json(doc_with_metadata)
    created_vector = neurons.create_vector(doc)
    database = get_supabase_db()
    database.set_file_sha_from_metadata(file_sha1)

    created_vector_id = created_vector[0]  # pyright: ignore reportPrivateUsage=none

    brain = Brain(id=brain_id)  # pyright: ignore
    brain.create_brain_vector(created_vector_id, file_sha1)
