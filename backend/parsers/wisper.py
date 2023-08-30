import os
import tempfile
import whisper
import openai
import time
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models.files import File
from models.settings import get_documents_vector_store
from utils.file import compute_sha1_from_content
from .common import process_file
from langchain.document_loaders import TextLoader


async def process_wisper(
    file: File,
    enable_summarization: bool,
    brain_id,
    user_openai_api_key,
):
    print('local wisper')
    temp_filename = None
    file_sha = ""
    dateshort = time.strftime("%Y%m%d-%H%M%S")
    file_meta_name = f"txt/audiotranscript_{dateshort}.txt"
    documents_vector_store = get_documents_vector_store()
    model = whisper.load_model("base")

    try:
        upload_file = file.file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=upload_file.filename,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            await upload_file.seek(0)  # pyright: ignore reportPrivateUsage=none
            content = (
                await upload_file.read()  # pyright: ignore reportPrivateUsage=none
            )
            tmp_file.write(content)
            tmp_file.flush()
            tmp_file.close()

            temp_filename = tmp_file.name
            transcript = model.transcribe(tmp_file.name)
            result = transcript["text"].encode('utf-8')

        file_sha = compute_sha1_from_content(
            result  # pyright: ignore reportPrivateUsage=none
        )

        file_size = len(
            result  # pyright: ignore reportPrivateUsage=none
        )

        chunk_size = 500
        chunk_overlap = 0

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        texts = text_splitter.split_text(
            transcript["text"]  # pyright: ignore reportPrivateUsage=none
        )

        docs_with_metadata = [
            Document(
                page_content=text,
                metadata={
                    "file_sha1": file_sha,
                    "file_size": file_size,
                    "file_name": file_meta_name,
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "date": dateshort,
                },
            )
            for text in texts
        ]

        documents_vector_store.add_documents(docs_with_metadata)
        process_file(
            file=result,
            loader_class=TextLoader,
            enable_summarization=enable_summarization,
            brain_id=brain_id,
            user_openai_api_key=user_openai_api_key,
        )
    finally:
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)
