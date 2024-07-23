import asyncio
import logging
from pathlib import Path
from pprint import PrettyPrinter
from typing import Any, AsyncGenerator, Callable, Dict, Self
from uuid import UUID, uuid4

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.vectorstores import VectorStore
from rich.console import Console
from rich.panel import Panel

from quivr_core.brain.info import BrainInfo, ChatHistoryInfo
from quivr_core.chat import ChatHistory
from quivr_core.config import RAGConfig
from quivr_core.files.file import load_qfile
from quivr_core.llm import LLMEndpoint
from quivr_core.models import ParsedRAGChunkResponse, ParsedRAGResponse, SearchResult
from quivr_core.processor.registry import get_processor_class
from quivr_core.quivr_rag import QuivrQARAG
from quivr_core.storage.local_storage import TransparentStorage
from quivr_core.storage.storage_base import StorageBase

from .brain_defaults import build_default_vectordb, default_embedder, default_llm

logger = logging.getLogger("quivr_core")


async def process_files(
    storage: StorageBase, skip_file_error: bool, **processor_kwargs: dict[str, Any]
) -> list[Document]:
    knowledge = []
    for file in await storage.get_files():
        try:
            if file.file_extension:
                processor_cls = get_processor_class(file.file_extension)
                logger.debug(f"processing {file} using class {processor_cls.__name__}")
                processor = processor_cls(**processor_kwargs)
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
        self._chats = self._init_chats()
        self.default_chat = list(self._chats.values())[0]

        # RAG dependencies:
        self.llm = llm
        self.vector_db = vector_db
        self.embedder = embedder

    def __repr__(self) -> str:
        pp = PrettyPrinter(width=80, depth=None, compact=False, sort_dicts=False)
        return pp.pformat(self.info())

    def print_info(self):
        console = Console()
        tree = self.info().to_tree()
        panel = Panel(tree, title="Brain Info", expand=False, border_style="bold")
        console.print(panel)

    def info(self) -> BrainInfo:
        # TODO: dim of embedding
        # "embedder": {},
        chats_info = ChatHistoryInfo(
            nb_chats=len(self._chats),
            current_default_chat=self.default_chat.id,
            current_chat_history_length=len(self.default_chat),
        )

        return BrainInfo(
            brain_id=self.id,
            brain_name=self.name,
            files_info=self.storage.info(),
            chats_info=chats_info,
            llm_info=self.llm.info(),
        )

    @property
    def chat_history(self) -> ChatHistory:
        return self.default_chat

    def _init_chats(self) -> Dict[UUID, ChatHistory]:
        chat_id = uuid4()
        default_chat = ChatHistory(chat_id=chat_id, brain_id=self.id)
        return {chat_id: default_chat}

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
        skip_file_error: bool = False,
    ):
        if llm is None:
            llm = default_llm()

        if embedder is None:
            embedder = default_embedder()

        brain_id = uuid4()

        # TODO: run in parallel using tasks

        for path in file_paths:
            file = await load_qfile(brain_id, path)
            await storage.upload_file(file)

        logger.debug(f"uploaded all files to {storage}")

        # Parse files
        docs = await process_files(
            storage=storage,
            skip_file_error=skip_file_error,
        )

        # Building brain's vectordb
        if vector_db is None:
            vector_db = await build_default_vectordb(docs, embedder)
        else:
            await vector_db.aadd_documents(docs)

        logger.debug(f"added {len(docs)} chunks to vectordb")

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
        skip_file_error: bool = False,
    ) -> Self:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            cls.afrom_files(
                name=name,
                file_paths=file_paths,
                vector_db=vector_db,
                storage=storage,
                llm=llm,
                embedder=embedder,
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
            llm = default_llm()

        if embedder is None:
            embedder = default_embedder()

        brain_id = uuid4()

        # Building brain's vectordb
        if vector_db is None:
            vector_db = await build_default_vectordb(langchain_documents, embedder)
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

        return [SearchResult(chunk=d, distance=s) for d, s in result]

    def get_chat_history(self, chat_id: UUID):
        return self._chats[chat_id]

    # TODO(@aminediro)
    def add_file(self) -> None:
        # add it to storage
        # add it to vectorstore
        raise NotImplementedError

    def ask(
        self,
        question: str,
        rag_config: RAGConfig | None = None,
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

        chat_history = self.default_chat

        parsed_response = rag_pipeline.answer(question, chat_history, [])

        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=parsed_response.answer))

        # Save answer to the chat history
        return parsed_response

    async def ask_streaming(
        self,
        question: str,
        rag_config: RAGConfig | None = None,
    ) -> AsyncGenerator[ParsedRAGChunkResponse, ParsedRAGChunkResponse]:
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

        chat_history = self.default_chat

        # TODO: List of files
        full_answer = ""
        async for response in rag_pipeline.answer_astream(question, chat_history, []):
            # Format output to be correct servicedf;j
            if not response.last_chunk:
                yield response
            full_answer += response.answer

        # TODO : add sources, metdata etc  ...
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=full_answer))
        yield response
