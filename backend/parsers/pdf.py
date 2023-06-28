from langchain.document_loaders import PyMuPDFLoader
from models.files import File
from models.settings import CommonsDep

from .common import process_file


def process_pdf(commons: CommonsDep, file: File, enable_summarization, brain_id, user_openai_api_key):
    return process_file(commons, file, PyMuPDFLoader, enable_summarization, brain_id, user_openai_api_key)

