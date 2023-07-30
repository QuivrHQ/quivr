from langchain.document_loaders import UnstructuredPowerPointLoader
from models.files import File
from models.settings import CommonsDep

from .common import process_file


def process_powerpoint(commons: CommonsDep, file: File, enable_summarization, brain_id, user_openai_api_key):
    return process_file(commons, file, UnstructuredPowerPointLoader, enable_summarization, brain_id, user_openai_api_key)
