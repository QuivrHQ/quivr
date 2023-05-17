from common import process_file
from langchain.document_loaders import TextLoader
from fastapi import UploadFile

async def process_txt(vector_store, file: UploadFile, stats_db):
    return await process_file(vector_store, file, TextLoader, stats_db=stats_db)