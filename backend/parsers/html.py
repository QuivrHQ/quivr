from .common import process_file
from langchain.document_loaders import UnstructuredHTMLLoader
import requests
import re
import unicodedata
import tempfile
import os
from fastapi import UploadFile


def process_html(file: UploadFile, enable_summarization):
    return process_file(file, UnstructuredHTMLLoader, ".html", enable_summarization)


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
