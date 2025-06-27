"""
Basic document retrieval node with runtime validation.
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
from quivr_core.rag.langgraph_framework.services.retrieval_service import (
    RetrievalService,
)
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.langgraph_framework.base.extractors import ConfigExtractor
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
            logger.info(f"Task ID: {task_id}")
            logger.info(f"Task definition: {tasks(task_id).definition}")
            # Create a separate retriever for each task to avoid session conflicts
            task_retriever = retrieval_service.get_basic_retriever()
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
