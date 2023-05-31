from fastapi import UploadFile
from langchain.document_loaders import TextLoader

from .common import process_file


async def process_txt(file: UploadFile, enable_summarization, user):
    return await process_file(file, TextLoader, ".txt", enable_summarization, user)
