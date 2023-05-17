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
from loaders.html import get_html, create_html_file, delete_tempfile
from loaders.powerpoint import process_powerpoint
from loaders.docx import process_docx
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
     ".pptx": process_powerpoint,
     ".docx": process_docx
}

def file_uploader(supabase, openai_key, vector_store):
    accept_multiple_files = st.secrets.self_hosted == "true"
    files = st.file_uploader("**Upload a file**", accept_multiple_files=accept_multiple_files, type=list(file_processors.keys()))
    if st.secrets.self_hosted == "false":
        st.markdown("**In demo mode, the max file size is 1MB**")
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
        if file_extension in file_processors:
            if st.secrets.self_hosted == "false":
                file_processors[file_extension](vector_store, file, stats_db=supabase)
            else:
                file_processors[file_extension](vector_store, file, stats_db=None)
            st.write(f"✅ {file.name} ")
            return True
        else:
            st.write(f"❌ {file.name} is not a valid file type.")
            return False

def url_uploader(supabase, openai_key, vector_store):
    
        url = st.text_area("**Add an url**",placeholder="https://www.quivr.app")
        button = st.button("Add the URL to the database")

        if button:
            if not st.session_state["overused"]:
                html = get_html(url)
                if html:
                    st.write(f"Getting content ... {url}  ")
                    file, temp_file_path = create_html_file(url, html)
                    ret = filter_file(file, supabase, vector_store)
                    delete_tempfile(temp_file_path, url, ret)
                else:
                    st.write(f"❌ Failed to access to {url} .")
            else:
                st.write("You have reached your daily limit. Please come back later or self host the solution.")
   

