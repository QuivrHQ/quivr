from abc import ABC, abstractmethod
from typing import List, Optional

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.retrievers import BaseRetriever


class RAGInterface(ABC):
    @abstractmethod
    def get_doc_chain(
        self,
        streaming: bool,
        callbacks: Optional[List[AsyncIteratorCallbackHandler]] = None,
    ) -> BaseCombineDocumentsChain:
        raise NotImplementedError(
            "get_doc_chain is an abstract method and must be implemented"
        )

    @abstractmethod
    def get_question_generation_llm(self) -> LLMChain:
        raise NotImplementedError(
            "get_question_generation_llm is an abstract method and must be implemented"
        )

    @abstractmethod
    def get_retriever(self) -> BaseRetriever:
        raise NotImplementedError(
            "get_retriever is an abstract method and must be implemented"
        )
