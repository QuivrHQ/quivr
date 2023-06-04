import os
import tempfile
import time
from io import BytesIO
from tempfile import NamedTemporaryFile

import openai
from fastapi import UploadFile
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.file import compute_sha1_from_content
from utils.vectors import documents_vector_store

# # Create a function to transcribe audio using Whisper
# def _transcribe_audio(api_key, audio_file, stats_db):
#     openai.api_key = api_key
#     transcript = ""

#     with BytesIO(audio_file.read()) as audio_bytes:
#         # Get the extension of the uploaded file
#         file_extension = os.path.splitext(audio_file.name)[-1]

#         # Create a temporary file with the uploaded audio data and the correct extension
#         with tempfile.NamedTemporaryFile(delete=True, suffix=file_extension) as temp_audio_file:
#             temp_audio_file.write(audio_bytes.read())
#             temp_audio_file.seek(0)  # Move the file pointer to the beginning of the file

#             transcript = openai.Audio.translate("whisper-1", temp_audio_file)

#     return transcript

# async def process_audio(upload_file: UploadFile, stats_db):
async def process_audio(upload_file: UploadFile, enable_summarization: bool, user):

    file_sha = ""
    dateshort = time.strftime("%Y%m%d-%H%M%S")
    file_meta_name = f"audiotranscript_{dateshort}.txt"
    # uploaded file to file object

    openai_api_key = os.environ.get("OPENAI_API_KEY")

    # Here, we're writing the uploaded file to a temporary file, so we can use it with your existing code.
    with tempfile.NamedTemporaryFile(delete=False, suffix=upload_file.filename) as tmp_file:
        await upload_file.seek(0)
        content = await upload_file.read()
        tmp_file.write(content)
        tmp_file.flush()
        tmp_file.close()

        with open(tmp_file.name, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

    file_sha = compute_sha1_from_content(transcript.text.encode("utf-8"))
    file_size = len(transcript.text.encode("utf-8"))

    # Load chunk size and overlap from sidebar
    chunk_size = 500
    chunk_overlap = 0

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_text(transcript)

    docs_with_metadata = [Document(page_content=text, metadata={"file_sha1": file_sha, "file_size": file_size, "file_name": file_meta_name,
                                   "chunk_size": chunk_size, "chunk_overlap": chunk_overlap, "date": dateshort}) for text in texts]

    # if st.secrets.self_hosted == "false":
    #     add_usage(stats_db, "embedding", "audio", metadata={"file_name": file_meta_name,"file_type": ".txt", "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})
    documents_vector_store.add_documents(docs_with_metadata)

    return documents_vector_store
