from langchain.document_loaders import UnstructuredPowerPointLoader
from models import File

from .common import process_file


def process_powerpoint(file: File, enable_summarization, brain_id, user_openai_api_key):
    return process_file(
        file=file,
        loader_class=UnstructuredPowerPointLoader,
        enable_summarization=enable_summarization,
        brain_id=brain_id,
        user_openai_api_key=user_openai_api_key,
    )
