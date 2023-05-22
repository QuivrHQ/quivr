from .common import process_file
from langchain.document_loaders import TextLoader
from fastapi import UploadFile


async def process_txt(file: UploadFile, enable_summarization):
    return await process_file(file, TextLoader, ".txt", enable_summarization)
