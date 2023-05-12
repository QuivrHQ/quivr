import streamlit as st
import os
from loaders.audio import process_audio
from loaders.txt import process_txt
from loaders.csv import process_csv
from loaders.markdown import process_markdown
from utils import compute_sha1_from_content
from loaders.pdf import process_pdf

def file_uploader(supabase, openai_key, vector_store):
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
    }

    files = st.file_uploader("Upload a file", accept_multiple_files=True, type=list(file_processors.keys()))
    if st.button("Add to Database"):
        if files is not None:
            for file in files:
                if file_already_exists(supabase, file):
                    st.write(f"😎 {file.name} is already in the database.")
                elif file.size < 1:
                    st.write(f"💨 {file.name} is empty.")
                else:
                    file_extension = os.path.splitext(file.name)[-1]
                    if file_extension in file_processors:
                        file_processors[file_extension](vector_store, file)
                        st.write(f"✅ {file.name} ")
                    else:
                        st.write(f"❌ {file.name} is not a valid file type.")

def file_already_exists(supabase, file):
    file_sha1 = compute_sha1_from_content(file.getvalue())
    response = supabase.table("documents").select("id").eq("metadata->>file_sha1", file_sha1).execute()
    return len(response.data) > 0