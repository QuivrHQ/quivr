"""
Document retrieval node with compression and reranking.
"""

import logging
from typing import Optional
import asyncio
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.entities.retrieval_service_config import (
    RetrievalServiceConfig,
)
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.langgraph_framework.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node
from quivr_core.rag.langgraph_framework.services.retrieval_service import (
    RetrievalService,
)

logger = logging.getLogger("quivr_core")


@register_node(
    name="compression_retrieve",
    description="Document retrieval with contextual compression and reranking",
    category="retrieval",
    version="1.0.0",
    dependencies=["retriever_service"],
)
class CompressionRetrievalNode(BaseNode):
    """
    Node for document retrieval with compression, reranking and filtering.
    """

    NODE_NAME = "compression_retrieve"

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
                "CompressionRetrievalNode requires 'messages' attribute in state"
            )
        if not state["messages"]:
            raise NodeValidationError(
                "CompressionRetrievalNode requires non-empty messages in state"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute document retrieval for all user tasks."""
        # Get configs
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
                (task_retriever.ainvoke(tasks(task_id).definition), task_id)
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
