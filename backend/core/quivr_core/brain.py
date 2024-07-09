import asyncio
import logging
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Self
from uuid import UUID, uuid4

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

from quivr_core.config import LLMEndpointConfig, RAGConfig
from quivr_core.llm import LLMEndpoint
from quivr_core.models import ParsedRAGResponse, SearchResult
from quivr_core.processor.default_parsers import DEFAULT_PARSERS
from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.quivr_rag import QuivrQARAG
from quivr_core.storage.file import QuivrFile
from quivr_core.storage.local_storage import TransparentStorage
from quivr_core.storage.storage_base import StorageBase

logger = logging.getLogger(__name__)


async def _default_vectordb(docs: list[Document], embedder: Embeddings) -> VectorStore:
    try:
        from langchain_community.vectorstores import FAISS

        logger.debug("Using Faiss-CPU as vector store.")
        # TODO(@aminediro) : embedding call is not concurrent for all documents but waits
        # We can actually wait on all processing
        if len(docs) > 0:
            vector_db = await FAISS.afrom_documents(documents=docs, embedding=embedder)
            return vector_db
        else:
            raise ValueError("can't initialize brain without documents")

    except ImportError as e:
        raise ImportError(
            "Please provide a valid vectore store or install quivr-core['base'] package for using the default one."
        ) from e


def _default_embedder() -> Embeddings:
    try:
        from langchain_openai import OpenAIEmbeddings

        logger.debug("Loaded OpenAIEmbeddings as default LLM for brain")
        embedder = OpenAIEmbeddings()
        return embedder
    except ImportError as e:
        raise ImportError(
            "Please provide a valid Embedder or install quivr-core['base'] package for using the defaultone."
        ) from e


def _default_llm() -> LLMEndpoint:
    try:
        logger.debug("Loaded ChatOpenAI as default LLM for brain")
        llm = LLMEndpoint.from_config(LLMEndpointConfig())
        return llm

    except ImportError as e:
        raise ImportError(
            "Please provide a valid BaseLLM or install quivr-core['base'] package"
        ) from e


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
        llm: LLMEndpoint,
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
        llm: LLMEndpoint | None = None,
        embedder: Embeddings | None = None,
        processors_mapping: Mapping[str, ProcessorBase] = DEFAULT_PARSERS,
        skip_file_error: bool = False,
    ):
        if llm is None:
            llm = _default_llm()

        if embedder is None:
            embedder = _default_embedder()

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
            vector_db = await _default_vectordb(docs, embedder)
        else:
            await vector_db.aadd_documents(docs)

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
        llm: LLMEndpoint | None = None,
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

    @classmethod
    async def afrom_langchain_documents(
        cls,
        *,
        name: str,
        langchain_documents: list[Document],
        vector_db: VectorStore | None = None,
        storage: StorageBase = TransparentStorage(),
        llm: LLMEndpoint | None = None,
        embedder: Embeddings | None = None,
    ) -> Self:
        if llm is None:
            llm = _default_llm()

        if embedder is None:
            embedder = _default_embedder()

        brain_id = uuid4()

        # Building brain's vectordb
        if vector_db is None:
            vector_db = await _default_vectordb(langchain_documents, embedder)
        else:
            await vector_db.aadd_documents(langchain_documents)

        return cls(
            id=brain_id,
            name=name,
            storage=storage,
            llm=llm,
            embedder=embedder,
            vector_db=vector_db,
        )

    async def asearch(
        self,
        query: str | Document,
        n_results: int = 5,
        filter: Callable | Dict[str, Any] | None = None,
        fetch_n_neighbors: int = 20,
    ) -> list[SearchResult]:
        result = await self.vector_db.asimilarity_search_with_score(
            query, k=n_results, filter=filter, fetch_k=fetch_n_neighbors
        )

        return [SearchResult(chunk=d, score=s) for d, s in result]

    # TODO(@aminediro)
    def add_file(self) -> None:
        # add it to storage
        # add it to vectorstore
        raise NotImplementedError

    def ask(
        self, question: str, rag_config: RAGConfig | None = None
    ) -> ParsedRAGResponse:
        llm = self.llm

        # If you passed a different llm model we'll override the brain  one
        if rag_config:
            if rag_config.llm_config != self.llm.get_config():
                llm = LLMEndpoint.from_config(config=rag_config.llm_config)
        else:
            rag_config = RAGConfig(llm_config=self.llm.get_config())

        rag_pipeline = QuivrQARAG(
            rag_config=rag_config, llm=llm, vector_store=self.vector_db
        )

        # transformed_history = format_chat_history(history)

        parsed_response = rag_pipeline.answer(question, [], [])

        # Save answer to the chat history
        return parsed_response
