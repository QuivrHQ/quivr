import time

from celery_task import create_embedding_for_document
from models import File
from repository.files.upload_file import DocumentSerializable


async def process_file(
    file: File,
    loader_class,
    enable_summarization,
    brain_id,
    user_openai_api_key,
):
    dateshort = time.strftime("%Y%m%d")

    file.compute_documents(loader_class)

    for doc in file.documents:  # pyright: ignore reportPrivateUsage=none
        metadata = {
            "file_sha1": file.file_sha1,
            "file_size": file.file_size,
            "file_name": file.file_name,
            "chunk_size": file.chunk_size,
            "chunk_overlap": file.chunk_overlap,
            "date": dateshort,
            "summarization": "true" if enable_summarization else "false",
        }
        doc_with_metadata = DocumentSerializable(
            page_content=doc.page_content, metadata=metadata
        )

        create_embedding_for_document.delay(
            brain_id, doc_with_metadata.to_json(), user_openai_api_key, file.file_sha1
        )

    return
