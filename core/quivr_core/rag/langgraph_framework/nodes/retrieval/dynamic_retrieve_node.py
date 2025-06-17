"""
Dynamic document retrieval node with adaptive search parameters.
"""

import logging
from typing import Optional, List
import asyncio
from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from langchain.retrievers import ContextualCompressionRetriever
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.nodes.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.nodes.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.nodes.retrieval.utils import (
    filter_chunks_by_relevance,
    get_compression_retriever,
)
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.entities.retriever import RetrieverConfig
from quivr_core.rag.entities.reranker import RerankerConfig
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node

logger = logging.getLogger("quivr_core")


@register_node(
    name="dynamic_retrieve",
    description="Dynamic document retrieval with adaptive search parameters based on relevance",
    category="retrieval",
    version="1.0.0",
    dependencies=["vector_store"],
)
class DynamicRetrievalNode(BaseNode):
    """
    Node for dynamic document retrieval with adaptive search parameters.
    """

    NODE_NAME = "dynamic_retrieve"
    CONFIG_TYPES = (RetrieverConfig, RerankerConfig)

    def __init__(
        self,
        vector_store: VectorStore,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(config_extractor, node_name, **kwargs)
        self.vector_store = vector_store
        self.retriever: Optional[ContextualCompressionRetriever] = None

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "messages" not in state:
            raise NodeValidationError(
                "DynamicRetrievalNode requires 'messages' attribute in state"
            )
        if not state["messages"]:
            raise NodeValidationError(
                "DynamicRetrievalNode requires non-empty messages in state"
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
        # Get configs
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
