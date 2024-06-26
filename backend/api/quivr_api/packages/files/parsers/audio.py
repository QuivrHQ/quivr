import time

import openai
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from quivr_api.models.files import File
from quivr_api.models.settings import get_documents_vector_store
from quivr_api.packages.files.file import compute_sha1_from_content


def process_audio(file: File, **kwargs):
    dateshort = time.strftime("%Y%m%d-%H%M%S")
    file_meta_name = f"audiotranscript_{dateshort}.txt"
    documents_vector_store = get_documents_vector_store()

    with open(file.tmp_file_path, "rb") as audio_file:
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

        documents_vector_store.add_documents(docs_with_metadata)
