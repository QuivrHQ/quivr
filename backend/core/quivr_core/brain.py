import logging
from pathlib import Path
from typing import Mapping, Self
from uuid import UUID, uuid4

from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.llms import BaseLLM
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAI

from quivr_core.config import RAGConfig
from quivr_core.models import ParsedRAGResponse
from quivr_core.processor.default_parsers import DEFAULT_PARSERS
from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.quivr_rag import QuivrQARAG
from quivr_core.storage.file import QuivrFile
from quivr_core.storage.local_storage import TransparentStorage
from quivr_core.storage.storage_base import StorageBase

logger = logging.getLogger(__name__)


def _process_files(
    storage: StorageBase,
    skip_file_error: bool,
    processors_mapping: Mapping[str, ProcessorBase],
) -> list[Document]:
    knowledge = []
    # Process files
    for file in storage.get_files():
        if file.file_extension:
            processor = processors_mapping[file.file_extension]
            docs = processor.process_file(file)
            knowledge.extend(docs)
        else:
            logger.error(f"can't find processor for {file}")
            if skip_file_error:
                continue
            else:
                raise Exception(f"Can't parse {file}. No available processor")

    return knowledge


class Brain:
    def __init__(
        self,
        *,
        name: str,
        id: UUID,
        vector_db,
        llm: BaseLLM,
        embedder: Embeddings,
        storage: StorageBase,
    ):
        self.id = id
        self.name = name
        self.storage = storage

        # Chat history
        self.chat_history: list[str] = []

        # RAG dependencies:
        self.llm = llm
        self.vector_db = vector_db
        self.embedder = embedder

    @classmethod
    def from_files(
        cls,
        *,
        name: str,
        file_paths: list[str | Path],
        vector_db: VectorStore | None = None,
        llm: BaseLLM = OpenAI(),
        storage: StorageBase = TransparentStorage(),
        embedder: Embeddings = OpenAIEmbeddings(),
        processors_mapping: Mapping[str, ProcessorBase] = DEFAULT_PARSERS,
        skip_file_error: bool = False,
    ) -> Self:
        brain_id = uuid4()

        for path in file_paths:
            file = QuivrFile.from_path(brain_id, path)
            storage.upload_file(file)

        # Parse files
        docs = _process_files(
            storage=storage,
            processors_mapping=processors_mapping,
            skip_file_error=skip_file_error,
        )

        # Building brain's vectordb
        if vector_db is None:
            vector_db = FAISS.from_documents(documents=docs, embedding=embedder)
        else:
            vector_db.add_documents(docs)

        return cls(
            id=brain_id,
            name=name,
            storage=storage,
            llm=llm,
            embedder=embedder,
            vector_db=vector_db,
        )

    # TODO(@aminediro)
    def add_file(self):
        # add it to storage
        # add it to vectorstore
        raise NotImplementedError

    def ask(
        self, question: str, rag_config: RAGConfig = RAGConfig()
    ) -> ParsedRAGResponse:
        rag_pipeline = QuivrQARAG(
            rag_config=rag_config, llm=self.llm, vector_store=self.vector_db
        )

        # transformed_history = format_chat_history(history)
        _list_files = self.storage.get_files()
        parsed_response = rag_pipeline.answer(question, [], [])

        # Save answer to the chat history
        return parsed_response
