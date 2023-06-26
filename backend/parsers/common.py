# from stats import add_usage
import asyncio
import os
import tempfile
import time
from typing import Optional

from fastapi import UploadFile
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models.brains import Brain
from models.settings import CommonsDep
from utils.file import compute_sha1_from_content, compute_sha1_from_file
from utils.vectors import Neurons, create_summary


async def process_file(
    commons: CommonsDep,
    file: UploadFile,
    loader_class,
    file_suffix,
    enable_summarization,
    brain_id,
    user_openai_api_key,
):
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
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    documents = text_splitter.split_documents(documents)

    for doc in documents:
        metadata = {
            "file_sha1": file_sha1,
            "file_size": file_size,
            "file_name": file_name,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "date": dateshort,
            "summarization": "true" if enable_summarization else "false",
        }
        doc_with_metadata = Document(
            page_content=doc.page_content, metadata=metadata)
        neurons = Neurons(commons=commons)
        created_vector = neurons.create_vector(doc_with_metadata, user_openai_api_key)
        # add_usage(stats_db, "embedding", "audio", metadata={"file_name": file_meta_name,"file_type": ".txt", "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})

        created_vector_id = created_vector[0]

        brain = Brain(id=brain_id)
        brain.create_brain_vector(created_vector_id)

        # Remove the enable_summarization and ids
        if enable_summarization and ids and len(ids) > 0:
            create_summary(
                commons, document_id=ids[0], content=doc.page_content, metadata=metadata
            )
    return


async def file_already_exists(supabase, file, brain_id):
    # TODO: user brain id instead of user
    file_content = await file.read()
    return await file_already_exists_from_content(supabase, file_content, brain_id)


async def file_already_exists_from_content(supabase, file_content, brain_id) -> bool:
    """
        Returns true if all vector_ids have a related entry in "brains_vectors"
    """
    file_sha1 = compute_sha1_from_content(file_content)
    response = (
        supabase.table("vectors")
        .select("id")
        .filter("metadata->>file_sha1", "eq", file_sha1)
        .execute()
    )
    vectors_ids = response.data

    print("vectors_ids", vectors_ids)
    print("len(vectors_ids)", len(vectors_ids))
    if len(vectors_ids) == 0:
        return False
    
    for vector in vectors_ids:
        response = (
            supabase.table("brains_vectors")
            .select("brain_id, vector_id")
            .filter("brain_id", "eq", brain_id)
            .filter("vector_id", "eq", vector['id'])
            .execute()
        )
        if len(response.data) == 0:
            return False
            
    return True