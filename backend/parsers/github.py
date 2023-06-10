import os
import time

from fastapi import UploadFile
from langchain.document_loaders import GitLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from parsers.common import file_already_exists_from_content
from utils.file import compute_sha1_from_content, compute_sha1_from_file
from utils.vectors import create_summary, create_vector, documents_vector_store

from .common import process_file


async def process_github(repo, enable_summarization, user, supabase, user_openai_api_key): 
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
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    documents = text_splitter.split_documents(documents)
    print(documents[:1])

    for doc in documents:
        if doc.metadata["file_type"] in [".pyc", ".env", ".lock", ".gitignore", ".gitmodules", ".gitattributes", ".gitkeep", ".git"]:
            continue
        metadata = {
            "file_sha1": compute_sha1_from_content(doc.page_content.encode("utf-8")),
            "file_size": len(doc.page_content)*8,
            "file_name": doc.metadata["file_name"],
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "date": dateshort,
            "summarization": "true" if enable_summarization else "false"
        }
        doc_with_metadata = Document(
            page_content=doc.page_content, metadata=metadata)
        exist = await file_already_exists_from_content(supabase, doc.page_content.encode("utf-8"), user)
        if not exist:
            create_vector(user.email, doc_with_metadata, user_openai_api_key)
            print("Created vector for ", doc.metadata["file_name"])

    return {"message": f"✅ Github with {len(documents)} files has been uploaded.", "type": "success"}

