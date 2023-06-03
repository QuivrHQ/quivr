# from stats import add_usage
import asyncio
import os
import tempfile
import time
from typing import Optional

from fastapi import UploadFile
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.file import compute_sha1_from_content, compute_sha1_from_file
from utils.vectors import create_summary, create_vector, documents_vector_store


async def process_file(file: UploadFile, loader_class, file_suffix, enable_summarization, user):
    documents = []
    file_name = file.filename
    file_size = file.file._file.tell()  # Getting the size of the file
    dateshort = time.strftime("%Y%m%d")

    # Here, we're writing the uploaded file to a temporary file, so we can use it with your existing code.
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp_file:
        await file.seek(0)
        content = await file.read()
        tmp_file.write(content)
        tmp_file.flush()

        loader = loader_class(tmp_file.name)
        documents = loader.load()
        # Ensure this function works with FastAPI
        file_sha1 = compute_sha1_from_file(tmp_file.name)

    os.remove(tmp_file.name)
    chunk_size = 500
    chunk_overlap = 0

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    documents = text_splitter.split_documents(documents)

    for doc in documents:
        metadata = {
            "file_sha1": file_sha1,
            "file_size": file_size,
            "file_name": file_name,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "date": dateshort,
            "summarization": "true" if enable_summarization else "false"
        }
        doc_with_metadata = Document(
            page_content=doc.page_content, metadata=metadata)
        create_vector(user.email, doc_with_metadata)
            #     add_usage(stats_db, "embedding", "audio", metadata={"file_name": file_meta_name,"file_type": ".txt", "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})

        if enable_summarization and ids and len(ids) > 0:
            create_summary(ids[0], doc.page_content, metadata)
    return


async def file_already_exists(supabase, file, user):
    file_content = await file.read()
    file_sha1 = compute_sha1_from_content(file_content)
    response = supabase.table("vectors").select("id").filter("metadata->>file_sha1", "eq", file_sha1) \
        .filter("user_id", "eq", user.email).execute()
    return len(response.data) > 0
