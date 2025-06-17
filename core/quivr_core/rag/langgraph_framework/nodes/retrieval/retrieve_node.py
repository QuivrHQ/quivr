"""
Basic document retrieval node with runtime validation.
"""

import logging
from typing import Optional
import asyncio
from langchain_core.vectorstores import VectorStore
from langchain_core.vectorstores import VectorStoreRetriever
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.nodes.base.node import (
    BaseNode,
    NodeValidationError,
)
from quivr_core.rag.langgraph_framework.nodes.retrieval.utils import get_retriever
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.entities.retriever import RetrieverConfig
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node

logger = logging.getLogger("quivr_core")


@register_node(
    name="retrieve",
    description="Basic document retrieval with reranking and filtering",
    category="retrieval",
    version="1.0.0",
    dependencies=["vector_store"],
)
class RetrievalNode(BaseNode):
    """
    Node for basic document retrieval with reranking and filtering.
    """

    NODE_NAME = "retrieve"
    CONFIG_TYPES = (RetrieverConfig,)

    def __init__(
        self,
        vector_store: VectorStore,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(config_extractor, node_name, **kwargs)
        self.vector_store = vector_store
        self.retriever: Optional[VectorStoreRetriever] = None

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
        # Get config
        retriever_config, retriever_config_changed = self.get_config(
            RetrieverConfig, config
        )

        if not self.retriever or retriever_config_changed:
            self.retriever = get_retriever(self.vector_store, retriever_config)

        if "tasks" in state:
            tasks = state["tasks"]
        else:
            tasks = UserTasks([state["messages"][0].content])

        if not tasks.has_tasks():
            return {**state}

        async_jobs = []
        for task_id in tasks.ids:
            async_jobs.append(
                (self.retriever.ainvoke(tasks(task_id).definition), task_id)
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
