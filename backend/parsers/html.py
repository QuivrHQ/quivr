import os
import re
import tempfile
import unicodedata

import requests
from fastapi import UploadFile
from langchain.document_loaders import UnstructuredHTMLLoader

from .common import process_file


def process_html(file: UploadFile, enable_summarization, user):
    return process_file(file, UnstructuredHTMLLoader, ".html", enable_summarization, user)


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text
