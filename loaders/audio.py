import os
import tempfile
from io import BytesIO
import time
import openai
import streamlit as st
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import compute_sha1_from_content, create_summary
from langchain.schema import Document
from stats import add_usage
from streamlit.logger import get_logger

logger = get_logger(__name__)

# Create a function to transcribe audio using Whisper


def _transcribe_audio(api_key, audio_file, stats_db):
    openai.api_key = api_key
    transcript = ""

    with BytesIO(audio_file.read()) as audio_bytes:
        # Get the extension of the uploaded file
        file_extension = os.path.splitext(audio_file.name)[-1]

        # Create a temporary file with the uploaded audio data and the correct extension
        with tempfile.NamedTemporaryFile(delete=True, suffix=file_extension) as temp_audio_file:
            temp_audio_file.write(audio_bytes.read())
            # Move the file pointer to the beginning of the file
            temp_audio_file.seek(0)

            # Transcribe the temporary audio file
            if st.secrets.self_hosted == "false":
                add_usage(stats_db, "embedding", "audio", metadata={
                          "file_name": audio_file.name, "file_type": file_extension})

            transcript = openai.Audio.translate("whisper-1", temp_audio_file)

    return transcript


def process_audio(vector_store, file_name, stats_db):
    if st.secrets.self_hosted == "false":
        if file_name.size > 10000000:
            st.error(
                "File size is too large. Please upload a file smaller than 1MB.")
            return
    file_sha = ""
    dateshort = time.strftime("%Y%m%d-%H%M%S")
    file_meta_name = f"audiotranscript_{dateshort}.txt"
    openai_api_key = st.secrets["openai_api_key"]
    transcript = _transcribe_audio(openai_api_key, file_name, stats_db)
    file_sha = compute_sha1_from_content(transcript.text.encode("utf-8"))
    # file size computed from transcript
    file_size = len(transcript.text.encode("utf-8"))

    # Load chunk size and overlap from sidebar
    chunk_size = st.session_state['chunk_size']
    chunk_overlap = st.session_state['chunk_overlap']

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_text(transcript.text)

    summarization = st.session_state['summarization']
    for text in texts:
        metadata = {
            "file_sha1": file_sha,
            "file_size": file_size,
            "file_name": file_meta_name,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "date": dateshort,
            "summarization": "true" if summarization else "false"
        }
        doc_with_metadata = Document(page_content=text, metadata=metadata)
        ids = vector_store.add_documents([doc_with_metadata])

        logger.info(f"Added document with id {ids}")
        if summarization and ids and len(ids) > 0:
            create_summary(ids[0], text, metadata)

    if st.secrets.self_hosted == "false":
        add_usage(stats_db, "embedding", "audio", metadata={
                  "file_name": file_meta_name, "file_type": ".txt", "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})
    return vector_store
