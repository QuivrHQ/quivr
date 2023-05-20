import tempfile
import time
import os
from utils import compute_sha1_from_file, create_summary
from langchain.schema import Document
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import SupabaseVectorStore
from stats import add_usage
from streamlit.logger import get_logger

logger = get_logger(__name__)


def process_file(vector_store: SupabaseVectorStore, file, loader_class, file_suffix, stats_db):
    documents = []
    file_name = file.name
    file_size = file.size
    if st.secrets.self_hosted == "false":
        if file_size > 1000000:
            st.error(
                "File size is too large. Please upload a file smaller than 1MB or self host.")
            return

    dateshort = time.strftime("%Y%m%d")
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
        tmp_file.write(file.getvalue())
        tmp_file.flush()

        loader = loader_class(tmp_file.name)
        documents = loader.load()
        file_sha1 = compute_sha1_from_file(tmp_file.name)

    os.remove(tmp_file.name)

    chunk_size = st.session_state['chunk_size']
    chunk_overlap = st.session_state['chunk_overlap']

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    documents = text_splitter.split_documents(documents)

    summarization = st.session_state['summarization']
    for doc in documents:
        metadata = {
            "file_sha1": file_sha1,
            "file_size": file_size,
            "file_name": file_name,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "date": dateshort,
            "summarization": "true" if summarization else "false"
        }
        doc_with_metadata = Document(
            page_content=doc.page_content, metadata=metadata)
        ids = vector_store.add_documents([doc_with_metadata])
        logger.info(f"Added document with id {ids}")
        if summarization and ids and len(ids) > 0:
            create_summary(ids[0], doc.page_content, metadata)

    if st.secrets.self_hosted == "false":
        add_usage(stats_db, "embedding", "file", metadata={
                  "file_name": file_name, "file_type": file_suffix, "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})
    return
