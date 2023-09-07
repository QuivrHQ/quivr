import os
import tempfile
import whisper
import time
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models import File
from utils.file import compute_sha1_from_content
from .common import vectorize
import openai


async def process_whisper(
    file: File,
    enable_summarization: bool,
    brain_id,
    user_openai_api_key,
):
    print('process whisper')
    dateshort = time.strftime("%Y%m%d-%H%M%S")
    file_meta_name = f"audiotranscript_{file.file.filename}_{dateshort}.txt"
    model = whisper.load_model("base")
    # get if to use whisper from local or from openAi
    if os.environ.get("WHISPER_LOCAL") == 'True':
        print("Running process on local")
        docs_with_metadata = await local_whisper(
            file,
            enable_summarization,
            model,
            file_meta_name,
            dateshort
        )
    else:
        docs_with_metadata = await openai_whisper(
            file,
            file_meta_name,
            dateshort
        )

    for doc_with_metadata in docs_with_metadata:
        await vectorize(
            doc_with_metadata,
            user_openai_api_key,
            brain_id,
            file.file_sha1,
        )


# using local whisper
async def local_whisper(
    file: File,
    enable_summarization: bool,
    model,
    file_meta_name,
    dateshort
):
    temp_filename = None
    file_sha = ""
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
                    "summarization": "true" if enable_summarization else "false",
                },
            )
            for text in texts
        ]

        return docs_with_metadata

    finally:
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)


# using cloud whisper
async def openai_whisper(
    file: File,
    file_meta_name,
    dateshort
):
    temp_filename = None
    file_sha = ""
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

            with open(tmp_file.name, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)

        file_sha = compute_sha1_from_content(
            transcript.text.encode("utf-8")  # pyright: ignore reportPrivateUsage=none
        )
        file_size = len(
            transcript.text.encode("utf-8")  # pyright: ignore reportPrivateUsage=none
        )

        chunk_size = 500
        chunk_overlap = 0

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        texts = text_splitter.split_text(
            transcript.text.encode("utf-8")  # pyright: ignore reportPrivateUsage=none
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

        return docs_with_metadata

    finally:
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)
