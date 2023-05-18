from typing import Optional
from fastapi import UploadFile
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from stats import add_usage
import asyncio
import os
import tempfile
import time
from utils import compute_sha1_from_file, compute_sha1_from_content

async def process_file(vector_store, file: UploadFile, loader_class, stats_db: Optional = None):
    documents = []
    file_sha = ""
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
        file_sha1 = compute_sha1_from_file(tmp_file.name)  # Ensure this function works with FastAPI

    os.remove(tmp_file.name)
    chunk_size = 500
    chunk_overlap = 0
    
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    print(documents)
    documents = text_splitter.split_documents(documents)


    # Add the document sha1 as metadata to each document
    docs_with_metadata = [Document(page_content=doc.page_content, metadata={"file_sha1": file_sha1, "file_size":file_size , "file_name": file_name, "chunk_size": chunk_size, "chunk_overlap": chunk_overlap, "date": dateshort}) for doc in documents]
    
    vector_store.add_documents(docs_with_metadata)
    # if stats_db:
    #     add_usage(stats_db, "embedding", "file", metadata={"file_name": file_name,"file_type": file.filename, "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})
    return

async def file_already_exists(supabase, file):
    file_content = await file.read()
    file_sha1 = compute_sha1_from_content(file_content)
    response = supabase.table("documents").select("id").eq("metadata->>file_sha1", file_sha1).execute()
    return len(response.data) > 0
