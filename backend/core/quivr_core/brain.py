import asyncio
import logging
from pathlib import Path
from typing import Mapping, Self
from uuid import UUID, uuid4

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStore

from quivr_core.config import RAGConfig
from quivr_core.models import ParsedRAGResponse
from quivr_core.processor.default_parsers import DEFAULT_PARSERS
from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.quivr_rag import QuivrQARAG
from quivr_core.storage.file import QuivrFile
from quivr_core.storage.local_storage import TransparentStorage
from quivr_core.storage.storage_base import StorageBase

logger = logging.getLogger(__name__)


async def _process_files(
    storage: StorageBase,
    skip_file_error: bool,
    processors_mapping: Mapping[str, ProcessorBase],
) -> list[Document]:
    knowledge = []
    for file in storage.get_files():
        try:
            if file.file_extension:
                processor = processors_mapping[file.file_extension]
                docs = await processor.process_file(file)
                knowledge.extend(docs)
            else:
                logger.error(f"can't find processor for {file}")
                if skip_file_error:
                    continue
                else:
                    raise ValueError(f"can't parse {file}. can't find file extension")
        except KeyError as e:
            if skip_file_error:
                continue
            else:
                raise Exception(f"Can't parse {file}. No available processor") from e

    return knowledge


class Brain:
    def __init__(
        self,
        *,
        name: str,
        id: UUID,
        vector_db: VectorStore,
        llm: BaseChatModel,
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
    async def afrom_files(
        cls,
        *,
        name: str,
        file_paths: list[str | Path],
        vector_db: VectorStore | None = None,
        storage: StorageBase = TransparentStorage(),
        llm: BaseChatModel | None = None,
        embedder: Embeddings | None = None,
        processors_mapping: Mapping[str, ProcessorBase] = DEFAULT_PARSERS,
        skip_file_error: bool = False,
    ):
        if llm is None:
            try:
                from langchain_openai import ChatOpenAI

                logger.debug("Loaded ChatOpenAI as default LLM for brain")

                llm = ChatOpenAI()

            except ImportError as e:
                raise ImportError(
                    "Please provide a valid BaseLLM or install quivr-core['base'] package"
                ) from e

        if embedder is None:
            try:
                from langchain_openai import OpenAIEmbeddings

                logger.debug("Loaded OpenAIEmbeddings as default LLM for brain")
                embedder = OpenAIEmbeddings()
            except ImportError as e:
                raise ImportError(
                    "Please provide a valid Embedder or install quivr-core['base'] package for using the defaultone."
                ) from e

        brain_id = uuid4()

        for path in file_paths:
            file = QuivrFile.from_path(brain_id, path)
            storage.upload_file(file)

        # Parse files
        docs = await _process_files(
            storage=storage,
            processors_mapping=processors_mapping,
            skip_file_error=skip_file_error,
        )

        # Building brain's vectordb
        if vector_db is None:
            try:
                from langchain_community.vectorstores import FAISS

                logger.debug("Using Faiss-CPU as vector store.")
                # TODO(@aminediro) : embedding call is not concurrent for all documents but waits
                # We can actually wait on all processing
                if len(docs) > 0:
                    vector_db = await FAISS.afrom_documents(
                        documents=docs, embedding=embedder
                    )
                else:
                    raise ValueError("can't initialize brain without documents")

            except ImportError as e:
                raise ImportError(
                    "Please provide a valid vectore store or install quivr-core['base'] package for using the default one."
                ) from e
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

    @classmethod
    def from_files(
        cls,
        *,
        name: str,
        file_paths: list[str | Path],
        vector_db: VectorStore | None = None,
        storage: StorageBase = TransparentStorage(),
        llm: BaseChatModel | None = None,
        embedder: Embeddings | None = None,
        processors_mapping: Mapping[str, ProcessorBase] = DEFAULT_PARSERS,
        skip_file_error: bool = False,
    ) -> Self:
        return asyncio.run(
            cls.afrom_files(
                name=name,
                file_paths=file_paths,
                vector_db=vector_db,
                storage=storage,
                llm=llm,
                embedder=embedder,
                processors_mapping=processors_mapping,
                skip_file_error=skip_file_error,
            )
        )

    # TODO(@aminediro)
    def add_file(self) -> None:
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
        parsed_response = rag_pipeline.answer(question, [], [])

        # Save answer to the chat history
        return parsed_response
