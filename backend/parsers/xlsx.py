from langchain.document_loaders import UnstructuredExcelLoader 
from models.files import File
from models.settings import CommonsDep

from .common import process_file


def process_xlsx(
    commons: CommonsDep,
    file: File,
    enable_summarization,
    brain_id,
    user_openai_api_key,
):
    return process_file(
        commons,
        file,
        UnstructuredExcelLoader,
        enable_summarization,
        brain_id,
        user_openai_api_key,
    )
