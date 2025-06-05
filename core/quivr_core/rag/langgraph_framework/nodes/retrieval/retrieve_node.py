"""
Basic document retrieval node with runtime validation.
"""

import logging
from typing import Optional, Dict, Any, Tuple
import asyncio

from quivr_core.rag.langgraph_framework.nodes.base.base_node import (
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
        retrieval_service: RetrievalService,
        config_extractor: ConfigExtractor,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)
        self.retrieval_service = retrieval_service

    def get_config(
        self, config: Optional[Dict[str, Any]] = None
    ) -> Tuple[RetrieverConfig, RerankerConfig]:
        """Extract and validate the filter history and LLM configs."""
        if config is None or not self.config_extractor:
            return RetrieverConfig(), RerankerConfig()

        retriever_dict, reranker_dict = self.config_extractor(config)

        return (
            RetrieverConfig.model_validate(retriever_dict),
            RerankerConfig.model_validate(reranker_dict),
        )

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""

        if "messages" not in state:
            raise NodeValidationError(
                "RetrieveNode requires 'messages' attribute in state"
            )

        if not state["messages"]:
            raise NodeValidationError(
                "RetrieveNode requires non-empty messages in state"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[Dict[str, Any]] = None):
        """Execute document retrieval for all user tasks."""

        # Get config using the injected extractor
        retrieval_config = self.get_config(config)
        if retrieval_config:
            retriever_config, reranker_config = retrieval_config
        else:
            retriever_config, reranker_config = RetrieverConfig(), RerankerConfig()

        if "tasks" in state:
            tasks = state["tasks"]
        else:
            tasks = UserTasks([state["messages"][0].content])

        if not tasks.has_tasks():
            return {**state}

        async_jobs = []
        for task_id in tasks.ids:
            # Create a tuple of the retrieval task and task_id
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
            tasks.set_docs(task_id, response)  # Associate docs with the specific task

        return {**state, "tasks": tasks}
