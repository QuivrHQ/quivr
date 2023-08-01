import requests
from langchain.document_loaders import UnstructuredHTMLLoader
from models.files import File

from .common import process_file


def process_html(
    file: File,
    enable_summarization,
    brain_id,
    user_openai_api_key,
):
    return process_file(
        file=file,
        loader_class=UnstructuredHTMLLoader,
        enable_summarization=enable_summarization,
        brain_id=brain_id,
        user_openai_api_key=user_openai_api_key,
    )


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None
