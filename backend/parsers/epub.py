from langchain.document_loaders.epub import UnstructuredEPubLoader
from models.files import File
from models.settings import CommonsDep

from .common import process_file


def process_epub(commons: CommonsDep, file: File, enable_summarization, brain_id, user_openai_api_key):
    return process_file(commons, file, UnstructuredEPubLoader, enable_summarization, brain_id, user_openai_api_key)
