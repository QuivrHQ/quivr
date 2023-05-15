import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec
import os
from loaders.audio import process_audio
from loaders.txt import process_txt
from loaders.csv import process_csv
from loaders.markdown import process_markdown
from loaders.html import process_html
from utils import compute_sha1_from_content
from loaders.pdf import process_pdf
import requests
import re
import unicodedata
import tempfile

file_processors = {
    ".txt": process_txt,
    ".csv": process_csv,
    ".md": process_markdown,
    ".markdown": process_markdown,
    ".m4a": process_audio,
    ".mp3": process_audio,
    ".webm": process_audio,
    ".mp4": process_audio,
    ".mpga": process_audio,
    ".wav": process_audio,
    ".mpeg": process_audio,
    ".pdf": process_pdf,
    ".html": process_html,
}

def file_uploader(supabase, openai_key, vector_store):
    files = st.file_uploader("Upload a file", accept_multiple_files=True, type=list(file_processors.keys()))
    if st.button("Add to Database"):
        if files is not None:
            for file in files:
                filter_file(file, supabase, vector_store)

def file_already_exists(supabase, file):
    file_sha1 = compute_sha1_from_content(file.getvalue())
    response = supabase.table("documents").select("id").eq("metadata->>file_sha1", file_sha1).execute()
    return len(response.data) > 0

def filter_file(file, supabase, vector_store):
    if file_already_exists(supabase, file):
        st.write(f"😎 {file.name} is already in the database.")
        return False
    elif file.size < 1:
        st.write(f"💨 {file.name} is empty.")
        return False
    else:
        file_extension = os.path.splitext(file.name)[-1]
        print(file.name, file_extension)
        if file_extension in file_processors:
            file_processors[file_extension](vector_store, file)
            st.write(f"✅ {file.name} ")
            return True
        else:
            st.write(f"❌ {file.name} is not a valid file type.")
            return False

def url_uploader(supabase, openai_key, vector_store):
    url = st.text_input("## Add an url",placeholder="https://www.quiver.app")
    button = st.button("Add the website page to the database")
    if button:
        html = get_html(url)
        if html:
            st.write(f"Getting content ... {url}  ")
            file, temp_file_path = create_html_file(url, html)
            ret = filter_file(file, supabase, vector_store)
            delete_tempfile(temp_file_path, url, ret)
        else:
            st.write(f"❌ Failed to access to {url} .")

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