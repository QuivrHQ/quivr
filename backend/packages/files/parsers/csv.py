from langchain.document_loaders import CSVLoader
from models import File

from .common import process_file


def process_csv(
    file: File,
    enable_summarization,
    brain_id,
    user_openai_api_key,
):
    return process_file(
        file=file,
        loader_class=CSVLoader,
        enable_summarization=enable_summarization,
        brain_id=brain_id,
        user_openai_api_key=user_openai_api_key,
    )
