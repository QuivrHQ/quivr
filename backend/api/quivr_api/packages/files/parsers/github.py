import os
import time

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import GitLoader
from quivr_api.models.files import File
from quivr_api.packages.embeddings.vectors import Neurons
from quivr_api.packages.files.file import compute_sha1_from_content


def process_github(
    repo,
    brain_id,
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
            "file_sha1": compute_sha1_from_content(doc.page_content.encode("utf-8")),
            "file_size": len(doc.page_content) * 8,
            "file_name": doc.metadata["file_name"],
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "date": dateshort,
            "original_file_name": doc.metadata["original_file_name"],
        }
        doc_with_metadata = Document(page_content=doc.page_content, metadata=metadata)

        print(doc_with_metadata.metadata["file_name"])

        file = File(
            file_sha1=compute_sha1_from_content(doc.page_content.encode("utf-8"))
        )

        file_exists = file.file_already_exists()

        if not file_exists:
            neurons = Neurons()
            created_vector = neurons.create_vector(doc_with_metadata)

        file_exists_in_brain = file.file_already_exists_in_brain(brain_id)

        if not file_exists_in_brain:
            file.link_file_to_brain(brain_id)
    return {
        "message": f"✅ Github with {len(documents)} files has been uploaded.",
        "type": "success",
    }
