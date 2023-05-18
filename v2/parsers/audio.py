import os
from tempfile import NamedTemporaryFile
import tempfile
from io import BytesIO
import time
import openai
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import compute_sha1_from_content
from langchain.schema import Document
from fastapi import UploadFile



async def process_audio(vector_store, upload_file: UploadFile, stats_db):
   
    file_sha = ""
    dateshort = time.strftime("%Y%m%d-%H%M%S")
    file_meta_name = f"audiotranscript_{dateshort}.txt"
    
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    file_extension = os.path.splitext(upload_file.filename)[-1]
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(await upload_file.read())
        temp_file_path = temp_file.name

        with open(temp_file_path, 'rb') as temp_file:
            transcript = openai.Audio.transcribe("whisper-1", temp_file)

            # Make sure to use the correct function, e.g., transcribe
            transcript = await openai.Audio.transcribe("whisper-1", temp_file)

            file_sha = compute_sha1_from_content(transcript.encode("utf-8"))
            ## file size computed from transcript
            file_size = len(transcript.encode("utf-8"))


            ## Load chunk size and overlap from sidebar
            chunk_size = 500
            chunk_overlap = 0

            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            print(transcript)
            print("#########")
            texts = text_splitter.split_text(transcript)

            docs_with_metadata = [Document(page_content=text, metadata={"file_sha1": file_sha,"file_size": file_size, "file_name": file_meta_name, "chunk_size": chunk_size, "chunk_overlap": chunk_overlap, "date": dateshort}) for text in texts]

            # if st.secrets.self_hosted == "false":
            #     add_usage(stats_db, "embedding", "audio", metadata={"file_name": file_meta_name,"file_type": ".txt", "chunk_size": chunk_size, "chunk_overlap": chunk_overlap})
            vector_store.add_documents(docs_with_metadata)
    os.unlink(temp_file.name)
    return vector_store

