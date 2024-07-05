from pathlib import Path
from uuid import UUID, uuid4

from langchain_core.embeddings import Embeddings
from langchain_core.language_models.llms import BaseLLM
from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAI

from quivr_core.processor.default_parsers import DEFAULT_PARSERS
from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.storage.file import QuivrFile
from quivr_core.storage.local_storage import TransparentStorage
from quivr_core.storage.storage_base import StorageBase


class Brain:
    def __init__(
        self,
        *,
        name: str,
        id: UUID,
        embedder: Embeddings | None = None,
        vector_store: VectorStore | None = None,
        llm: BaseLLM = OpenAI(),
        processors_mapping: dict[str, ProcessorBase] = DEFAULT_PARSERS,
        storage: StorageBase = TransparentStorage(),
        # retriever=KeyWordRetriever(),
    ):
        self.id = id
        self.name = name
        self.storage = storage

        # Chat history
        self.chat_history: list[str] = []

        # Doc parsing deps
        self.processors_mapping = processors_mapping

        # Rag dependencies:
        self.llm = llm
        self.vector_store = vector_store
        self.embedder = embedder

    @classmethod
    def from_directory(cls, documents: list[str | Path], recursive: bool = True):
        pass

    @classmethod
    def from_files(
        cls,
        *,
        name: str,
        file_paths: list[str | Path],
        storage: StorageBase = TransparentStorage(),
    ):
        brain_id = uuid4()
        files = [QuivrFile.from_path(brain_id, path) for path in file_paths]

        # Build the storage
        [storage.upload_file(file) for file in files]

        return cls(id=brain_id, name=name, storage=storage)

    def ask(self, question: str):
        # rag_config, llm, vector_store
        pass
