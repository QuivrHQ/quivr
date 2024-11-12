import logging
import os

import spacy
import aiofiles
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter

from quivr_core.files.file import QuivrFile
from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.processor.registry import FileExtension
from quivr_core.processor.splitter import SplitterConfig

logger = logging.getLogger("quivr_core")


class SpaCyProcessor(ProcessorBase):
    """
    SpaCyProcessor for handling various text file types with spaCy NLP.

    It extracts and processes text content using spaCy's NLP pipeline.

    ## Installation
    ```bash
    pip install spacy pandas
    python -m spacy download en_core_web_sm
    ```
    """

    supported_extensions = [
        FileExtension.pdf,
        FileExtension.docx,
        FileExtension.txt,
        FileExtension.csv,
    ]

    def __init__(
        self,
        splitter: TextSplitter | None = None,
        splitter_config: SplitterConfig = SplitterConfig(),
        spacy_model: str = "en_core_web_sm"
    ) -> None:
        self.nlp = spacy.load(spacy_model)
        self.splitter_config = splitter_config

        if splitter:
            self.text_splitter = splitter
        else:
            self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=splitter_config.chunk_size,
                chunk_overlap=splitter_config.chunk_overlap,
            )

    @property
    def processor_metadata(self):
        return {
            "processor_cls": "SpaCyProcessor",
            "chunk_overlap": self.splitter_config.chunk_overlap,
        }

    async def process_file_inner(self, file: QuivrFile) -> list[Document]:
        # Extract text based on file type
        if file.extension == FileExtension.pdf:
            text = await self.extract_text_from_pdf(file)
        elif file.extension == FileExtension.docx:
            text = await self.extract_text_from_docx(file)
        elif file.extension == FileExtension.txt:
            text = await self.extract_text_from_txt(file)
        elif file.extension == FileExtension.csv:
            text = await self.extract_text_from_csv(file)
        else:
            raise ValueError(f"Unsupported file type: {file.extension}")

        # Apply spaCy NLP processing
        doc = Document(page_content=text)
        processed_docs = self.text_splitter.split_documents([doc])

        for doc in processed_docs:
            doc.metadata = {"chunk_size": len(self.nlp(doc.page_content))}
            # Run spaCy NLP on each chunk
            doc.page_content = self.nlp(doc.page_content).text

        return processed_docs

    async def extract_text_from_pdf(self, file: QuivrFile) -> str:
        # Placeholder for PDF text extraction
        async with file.open() as f:
            # PDF text extraction logic here
            return "Extracted PDF text"

    async def extract_text_from_docx(self, file: QuivrFile) -> str:
        # Placeholder for DOCX text extraction
        async with file.open() as f:
            # DOCX text extraction logic here
            return "Extracted DOCX text"

    async def extract_text_from_txt(self, file: QuivrFile) -> str:
        async with aiofiles.open(file.path, mode="r") as f:
            content = await f.read()
        return content

    async def extract_text_from_csv(self, file: QuivrFile) -> str:
        df = pd.read_csv(file.path)
        return ' '.join(df.astype(str).values.flatten())
