import os
import time

from langchain.document_loaders import GitLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models import Brain, File
from utils.file import compute_sha1_from_content
from utils.vectors import Neurons


async def process_github(
    repo,
    enable_summarization,
    brain_id,
    user_openai_api_key,
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
            "summarization": "true" if enable_summarization else "false",
        }
        doc_with_metadata = Document(page_content=doc.page_content, metadata=metadata)

        file = File(
            file_sha1=compute_sha1_from_content(doc.page_content.encode("utf-8"))
        )

        file_exists = file.file_already_exists()

        if not file_exists:
            neurons = Neurons()
            created_vector = neurons.create_vector(
                doc_with_metadata, user_openai_api_key
            )

        file_exists_in_brain = file.file_already_exists_in_brain(brain_id)

        if not file_exists_in_brain:
            brain = Brain(id=brain_id)
            file.link_file_to_brain(brain)
    return {
        "message": f"✅ Github with {len(documents)} files has been uploaded.",
        "type": "success",
    }
