"""
Basic document retrieval node with runtime validation.
"""

import logging
from typing import Optional
import asyncio
from langchain_core.vectorstores import VectorStore

from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.nodes.base.node import (
    BaseNode,
    NodeValidationError,
)
from quivr_core.rag.langgraph_framework.services.retrieval_service import (
    RetrievalService,
)
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.entities.retriever import RetrieverConfig
from quivr_core.rag.entities.reranker import RerankerConfig
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor

logger = logging.getLogger("quivr_core")


class RetrievalNode(BaseNode):
    """
    Node for basic document retrieval with reranking and filtering.

    Runtime Requirements: State must have:
    - tasks: UserTasks (for reading tasks)
    - with_documents(docs) method (for writing documents)
    - with_reasoning(reasoning) method (for writing reasoning)
    """

    NODE_NAME = "retrieve"
    CONFIG_TYPES = (RetrieverConfig, RerankerConfig)

    def __init__(
        self,
        retrieval_service: Optional[RetrievalService] = None,
        vector_store: Optional[VectorStore] = None,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)

        self.retrieval_service = retrieval_service
        self._retrieval_service_user_provided = retrieval_service is not None

        self.vector_store = vector_store

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

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute document retrieval for all user tasks."""
        # Type-safe config extraction
        retriever_config, _ = self.get_config(RetrieverConfig, config)
        reranker_config, _ = self.get_config(RerankerConfig, config)

        # Initialize RetrievalService if needed
        if not self.retrieval_service:
            self.logger.debug(
                "Initializing/reinitializing RetrievalService due to config change"
            )
            assert self.vector_store, "Vector store is required for RetrievalService"
            self.retrieval_service = RetrievalService(vector_store=self.vector_store)
        assert self.retrieval_service

        if "tasks" in state:
            tasks = state["tasks"]
        else:
            tasks = UserTasks([state["messages"][0].content])

        if not tasks.has_tasks():
            return {**state}

        async_jobs = []
        for task_id in tasks.ids:
            if retriever_config.dynamic_retrieval:
                async_jobs.append(
                    (
                        self.retrieval_service.retrieve_documents_dynamic(
                            query=tasks(task_id).definition,
                            reranker_config=reranker_config,
                            retriever_config=retriever_config,
                        ),
                        task_id,
                    )
                )
            else:
                async_jobs.append(
                    (
                        self.retrieval_service.retrieve_documents(
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
