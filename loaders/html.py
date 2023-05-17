from .common import process_file
from langchain.document_loaders import UnstructuredHTMLLoader
import requests
import re
import unicodedata
import tempfile
import os
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFileRec, UploadedFile

def process_html(vector_store, file, stats_db):
    return process_file(vector_store, file, UnstructuredHTMLLoader, ".html", stats_db=stats_db)


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def create_html_file(url, content):
    file_name = slugify(url) + ".html"
    temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(content)

    record = UploadedFileRec(id=None, name=file_name, type='text/html', data=open(temp_file_path, 'rb').read())
    uploaded_file = UploadedFile(record)
    
    return uploaded_file, temp_file_path

def delete_tempfile(temp_file_path, url, ret):
    try:
        os.remove(temp_file_path)
        if ret:
            st.write(f"✅ Content saved... {url}  ")
    except OSError as e:
        print(f"Error while deleting the temporary file: {str(e)}")
        if ret:
            st.write(f"❌ Error while saving content... {url}  ")

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text