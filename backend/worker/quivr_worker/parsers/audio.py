import time

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI

from quivr_worker.files import File, compute_sha1


def process_audio(file: File, model: str = "whisper=1"):
    # TODO(@aminediro): These should apear in the class processor
    # Should be instanciated once per Processor
    chunk_size = 500
    chunk_overlap = 0
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    client = OpenAI()

    dateshort = time.strftime("%Y%m%d-%H%M%S")
    file_meta_name = f"audiotranscript_{dateshort}.txt"
    with open(file.tmp_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model=model, file=audio_file)
        transcript_txt = transcript.text.encode("utf-8")

        file_size, file_sha1 = len(transcript_txt), compute_sha1(transcript_txt)
        texts = text_splitter.split_text(transcript.text)

        docs_with_metadata = [
            Document(
                page_content=text,
                metadata={
                    "file_sha1": file_sha1,
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
