import os
import time

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import GitLoader
from quivr_api.models.settings import get_documents_vector_store
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService

from quivr_worker.files import File
from quivr_worker.parsers.common import upload_vector_docs


def link_file_to_brain(self, brain_id):
    self.set_file_vectors_ids()

    if self.vectors_ids is None:
        return

    brain_vector_service = BrainVectorService(brain_id)

    for vector_id in self.vectors_ids:  # pyright: ignore reportPrivateUsage=none
        brain_vector_service.create_brain_vector(vector_id["id"], self.file_sha1)


def process_github(
    repo,
    brain_id,
    supabase_vector_store=get_documents_vector_store(),
):
    random_dir_name = os.urandom(16).hex()
    dateshort = time.strftime("%Y%m%d")
    loader = GitLoader(
        clone_url=repo,
        repo_path="/tmp/" + random_dir_name,
    )
    documents = loader.load()
    os.system("rm -rf /tmp/" + random_dir_name)

    chunk_size = 500
    chunk_overlap = 0
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    documents = text_splitter.split_documents(documents)
    for doc in documents:
        sha1 = compute_sha1_from_content(doc.page_content.encode("utf-8"))
        if doc.metadata["file_type"] in [
            ".pyc",
            ".png",
            ".svg",
            ".env",
            ".lock",
            ".gitignore",
            ".gitmodules",
            ".gitattributes",
            ".gitkeep",
            ".git",
            ".json",
        ]:
            continue
        metadata = {
            "file_sha1": sha1,
            "file_size": len(doc.page_content) * 8,
            "file_name": doc.metadata["file_name"],
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "date": dateshort,
            "original_file_name": doc.metadata["original_file_name"],
        }
        doc_with_metadata = Document(page_content=doc.page_content, metadata=metadata)

        print(doc_with_metadata.metadata["file_name"])

        file = File(file_sha1=sha1)
        file_exists = file.file_already_exists()

        if not file_exists:
            upload_vector_docs([doc_with_metadata], supabase_vector_store)

        file_exists_in_brain = file.file_already_exists_in_brain(brain_id)

        if not file_exists_in_brain:
            file.link_file_to_brain(brain_id)
    return {
        "message": f"✅ Github with {len(documents)} files has been uploaded.",
        "type": "success",
    }
