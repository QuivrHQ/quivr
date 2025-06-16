"""
Basic document retrieval node with runtime validation.
"""

import logging
from typing import Optional
import asyncio
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from typing import List
from langchain.retrievers import ContextualCompressionRetriever
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.nodes.base.node import (
    BaseNode,
    NodeValidationError,
)
from quivr_core.rag.langgraph_framework.nodes.retrieval.utils import (
    filter_chunks_by_relevance,
    get_compression_retriever,
)

from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.entities.retriever import RetrieverConfig
from quivr_core.rag.entities.reranker import RerankerConfig
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor

logger = logging.getLogger("quivr_core")


class DynamicRetrievalNode(BaseNode):
    """
    Node for basic document retrieval with reranking and filtering.

    Runtime Requirements: State must have:
    - tasks: UserTasks (for reading tasks)
    - with_documents(docs) method (for writing documents)
    - with_reasoning(reasoning) method (for writing reasoning)
    """

    NODE_NAME = "retrieve"
    CONFIG_TYPES = (RetrieverConfig,)

    def __init__(
        self,
        vector_store: VectorStore,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)

        self.vector_store = vector_store
        self.retriever: Optional[ContextualCompressionRetriever] = None

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "messages" not in state:
            raise NodeValidationError(
                "RetrievalNode requires 'messages' attribute in state"
            )

        if not state["messages"]:
            raise NodeValidationError(
                "RetrievalNode requires non-empty messages in state"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def _dynamic_retrieve(
        self,
        query: str,
        reranker_config: RerankerConfig,
        retriever_config: RetrieverConfig,
    ) -> List[Document]:
        """
        Dynamically retrieve documents, increasing search parameters if needed.

        Args:
            query: The search query
            filter_dict: Optional filter to apply to search
            max_iterations: Maximum number of retrieval attempts
            **kwargs: Additional arguments for retrieval configuration

        Returns:
            List of retrieved and filtered documents
        """
        top_n = reranker_config.top_n
        k = retriever_config.k

        number_of_relevant_chunks = top_n
        iteration = 1

        while (
            number_of_relevant_chunks == top_n
            and iteration <= retriever_config.dynamic_retrieval_max_iterations
        ):
            current_top_n = top_n * iteration
            current_k = max([current_top_n * 2, k])

            if iteration > 1:
                logger.info(
                    f"Increasing top_n to {current_top_n} and k to {current_k} "
                    "to retrieve more relevant chunks"
                )

            assert self.retriever, "Retriever not initialized"
            docs = await self.retriever.ainvoke(query)

            filtered_docs = filter_chunks_by_relevance(
                docs,
                relevance_score_threshold=reranker_config.relevance_score_threshold,
                relevance_score_key=reranker_config.relevance_score_key,
            )

            number_of_relevant_chunks = len(filtered_docs)
            iteration += 1

            # If we got fewer docs than requested, no need to continue
            if number_of_relevant_chunks < current_top_n:
                break

        return filtered_docs

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute document retrieval for all user tasks."""
        retriever_config, retriever_config_changed = self.get_config(
            RetrieverConfig, config
        )

        reranker_config, reranker_config_changed = self.get_config(
            RerankerConfig, config
        )

        if not self.retriever or retriever_config_changed or reranker_config_changed:
            self.retriever = get_compression_retriever(
                self.vector_store, retriever_config, reranker_config
            )

        if "tasks" in state:
            tasks = state["tasks"]
        else:
            tasks = UserTasks([state["messages"][0].content])

        if not tasks.has_tasks():
            return {**state}

        async_jobs = []
        for task_id in tasks.ids:
            async_jobs.append(
                (
                    self._dynamic_retrieve(
                        query=tasks(task_id).definition,
                        reranker_config=reranker_config,
                        retriever_config=retriever_config,
                    ),
                    task_id,
                )
            )

        # Gather all the responses asynchronously
        responses = (
            await asyncio.gather(*(task[0] for task in async_jobs))
            if async_jobs
            else []
        )
        task_ids = [task[1] for task in async_jobs] if async_jobs else []

        # Process responses and associate docs with tasks
        for response, task_id in zip(responses, task_ids, strict=False):
            tasks.set_docs(task_id, response)

        return {**state, "tasks": tasks}
