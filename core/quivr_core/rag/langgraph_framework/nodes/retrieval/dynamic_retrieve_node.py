"""
Dynamic document retrieval node with adaptive search parameters.
"""

import logging
from typing import Optional, List
import asyncio
from langchain_core.documents import Document
from langchain.retrievers import ContextualCompressionRetriever
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.entities.retrieval_service_config import (
    RetrievalServiceConfig,
)
from quivr_core.rag.langgraph_framework.services.utils import (
    filter_chunks_by_relevance,
)
from quivr_core.rag.langgraph_framework.services.retrieval_service import (
    RetrievalService,
)
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.langgraph_framework.base.extractors import ConfigExtractor
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

    def __init__(
        self,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(config_extractor, node_name, **kwargs)

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
        retriever: ContextualCompressionRetriever,
        retrieval_service_config: RetrievalServiceConfig,
    ) -> List[Document]:
        """
        Dynamically retrieve documents, increasing search parameters if needed.
        """
        top_n = retrieval_service_config.reranker_config.top_n
        k = retrieval_service_config.retriever_config.k

        number_of_relevant_chunks = top_n
        iteration = 1

        while (
            number_of_relevant_chunks == top_n
            and iteration
            <= retrieval_service_config.retriever_config.extra_config.dynamic_retrieval_max_iterations
        ):
            current_top_n = top_n * iteration
            current_k = max([current_top_n * 2, k])

            if iteration > 1:
                logger.info(
                    f"Increasing top_n to {current_top_n} and k to {current_k} "
                    "to retrieve more relevant chunks"
                )

            docs = await retriever.ainvoke(query)

            filtered_docs = filter_chunks_by_relevance(
                docs,
                relevance_score_threshold=retrieval_service_config.reranker_config.relevance_score_threshold,
                relevance_score_key=retrieval_service_config.reranker_config.relevance_score_key,
            )

            number_of_relevant_chunks = len(filtered_docs)
            iteration += 1

            # If we got fewer docs than requested, no need to continue
            if number_of_relevant_chunks < current_top_n:
                break

        return filtered_docs

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute document retrieval for all user tasks."""

        retrieval_service_config = self.get_config(RetrievalServiceConfig, config)

        # Get retriever service
        retrieval_service = self.get_service(RetrievalService, retrieval_service_config)

        if "tasks" in state:
            tasks = state["tasks"]
        else:
            tasks = UserTasks([state["messages"][0].content])

        if not tasks.has_tasks():
            return {**state}

        async_jobs = []
        for task_id in tasks.ids:
            # Create a separate retriever for each task to avoid session conflicts
            task_retriever = retrieval_service.get_compression_retriever()
            async_jobs.append(
                (
                    self._dynamic_retrieve(
                        query=tasks(task_id).definition,
                        retriever=task_retriever,
                        retrieval_service_config=retrieval_service_config,
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
