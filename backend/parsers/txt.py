from fastapi import UploadFile
from langchain.document_loaders import TextLoader
from models.settings import CommonsDep

from .common import process_file


async def process_txt(commons: CommonsDep, file: UploadFile, enable_summarization, user, user_openai_api_key):
    return await process_file(commons, file, TextLoader, ".txt", enable_summarization, user,user_openai_api_key)
