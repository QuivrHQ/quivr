import os
from typing import (
    Any,
    Union,
)
import zipfile
import streamlit as st
from streamlit.runtime.uploaded_file_manager import (
    UploadedFile,
    UploadedFileRec,
    UploadedFileManager,
)
from streamlit.runtime.scriptrunner import get_script_run_ctx
from supabase.client import Client
from langchain.vectorstores.supabase import SupabaseVectorStore
from components_keys import ComponentsKeys
from loaders.audio import process_audio
from loaders.txt import process_txt
from loaders.csv import process_csv
from loaders.markdown import process_markdown
from loaders.pdf import process_pdf
from loaders.html import (
    create_html_file,
    delete_tempfile,
    get_html,
    process_html,
)
from loaders.powerpoint import process_powerpoint
from loaders.docx import process_docx
from utils import compute_sha1_from_content


ctx = get_script_run_ctx()
manager = UploadedFileManager()
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

def file_uploader(supabase, vector_store):
    # Omit zip file support if the `st.secrets.self_hosted` != "true" because
    # a zip file can consist of multiple files so the limit on 1 file uploaded
    # at a time in the demo can be circumvented.
    accepted_file_extensions = list(file_processors.keys())
    accept_multiple_files = st.secrets.self_hosted == "true"
    if accept_multiple_files:
        accepted_file_extensions += [".zip"]

    files = st.file_uploader(
        "**Upload a file**",
        accept_multiple_files=accept_multiple_files,
        type=accepted_file_extensions,
        key=ComponentsKeys.FILE_UPLOADER,
    )
    if st.secrets.self_hosted == "false":
        st.markdown("**In demo mode, the max file size is 1MB**")
    if st.button("Add to Database"):
        # Single file upload
        if isinstance(files, UploadedFile):
            filter_file(files, supabase, vector_store)
        # Multiple files upload
        elif isinstance(files, list):
            for file in files:
                filter_file(file, supabase, vector_store)

def file_already_exists(supabase, file):
    file_sha1 = compute_sha1_from_content(file.getvalue())
    response = supabase.table("documents").select("id").eq("metadata->>file_sha1", file_sha1).execute()
    return len(response.data) > 0

def file_to_uploaded_file(file: Any) -> Union[None, UploadedFile]:
    """Convert a file to a streamlit `UploadedFile` object.

    This allows us to unzip files and treat them the same way
    streamlit treats files uploaded through the file uploader.

    Parameters
    ---------
    file : Any
        The file. Can be any file supported by this app.

    Returns
    -------
    Union[None, UploadedFile]
        The file converted to a streamlit `UploadedFile` object.
        Returns `None` if the script context cannot be grabbed.
    """

    if ctx is None:
        print("script context not found, skipping uploading file:", file.name)
        return

    file_extension = os.path.splitext(file.name)[-1]
    file_name = file.name
    file_data = file.read()
    # The file manager will automatically assign an ID so pass `None`
    # Reference: https://github.com/streamlit/streamlit/blob/9a6ce804b7977bdc1f18906d1672c45f9a9b3398/lib/streamlit/runtime/uploaded_file_manager.py#LL98C6-L98C6
    uploaded_file_rec = UploadedFileRec(None, file_name, file_extension, file_data)
    uploaded_file_rec = manager.add_file(
        ctx.session_id,
        ComponentsKeys.FILE_UPLOADER,
        uploaded_file_rec,
    )
    return UploadedFile(uploaded_file_rec)

def filter_zip_file(
    file: UploadedFile,
    supabase: Client,
    vector_store: SupabaseVectorStore,
) -> None:
    """Unzip the zip file then filter each unzipped file.

    Parameters
    ----------
    file : UploadedFile
        The uploaded file from the file uploader.
    supabase : Client
        The supabase client.
    vector_store : SupabaseVectorStore
        The vector store in the database.
    """

    with zipfile.ZipFile(file, "r") as z:
        unzipped_files = z.namelist()
        for unzipped_file in unzipped_files:
            with z.open(unzipped_file, "r") as f:
                filter_file(f, supabase, vector_store)

def filter_file(file, supabase, vector_store):
    # Streamlit file uploads are of type `UploadedFile` which has the
    # necessary methods and attributes for this app to work.
    if not isinstance(file, UploadedFile):
        file = file_to_uploaded_file(file)

    file_extension = os.path.splitext(file.name)[-1]
    if file_extension == ".zip":
        filter_zip_file(file, supabase, vector_store)
        return True

    if file_already_exists(supabase, file):
        st.write(f"😎 {file.name} is already in the database.")
        return False

    if file.size < 1:
        st.write(f"💨 {file.name} is empty.")
        return False

    if file_extension in file_processors:
        if st.secrets.self_hosted == "false":
            file_processors[file_extension](vector_store, file, stats_db=supabase)
        else:
            file_processors[file_extension](vector_store, file, stats_db=None)
        st.write(f"✅ {file.name} ")
        return True

    st.write(f"❌ {file.name} is not a valid file type.")
    return False

def url_uploader(supabase, vector_store):
    url = st.text_area("**Add an url**",placeholder="https://www.quivr.app")
    button = st.button("Add the URL to the database")

    if button:
        if not st.session_state["overused"]:
            html = get_html(url)
            if html:
                st.write(f"Getting content ... {url}  ")
                try:
                    file, temp_file_path = create_html_file(url, html)
                except UnicodeEncodeError as e:
                    st.write(f"❌ Error encoding character: {e}")
                file, temp_file_path = create_html_file(url, html)
                ret = filter_file(file, supabase, vector_store)
                delete_tempfile(temp_file_path, url, ret)
            else:
                st.write(f"❌ Failed to access to {url} .")
        else:
            st.write("You have reached your daily limit. Please come back later or self host the solution.")