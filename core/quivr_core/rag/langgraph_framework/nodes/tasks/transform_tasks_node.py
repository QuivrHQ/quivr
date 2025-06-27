from typing import Optional
import asyncio
from quivr_core.rag.entities.config import LLMEndpointConfig
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.services.rag_prompt_service import (
    RAGPromptService,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node
import logging

logger = logging.getLogger("quivr_core")


@register_node(
    name="transform_tasks",
    description="Transform and refine user tasks using LLM processing",
    category="tasks",
    version="1.0.0",
    dependencies=["llm_service", "prompt_service"],
)
class TransformTasksNode(BaseNode):
    """
    Node for transforming user tasks.
    """

    NODE_NAME = "transform_tasks"

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        # Validate messages (used for fallback task creation)
        if "messages" not in state:
            raise NodeValidationError(
                "TransformTasksNode requires 'messages' attribute in state"
            )

        if not state["messages"]:
            raise NodeValidationError(
                "TransformTasksNode requires non-empty messages in state"
            )

        # Validate chat_history
        if "chat_history" not in state:
            raise NodeValidationError(
                "TransformTasksNode requires 'chat_history' attribute in state"
            )

        # Validate chat_history has required methods
        chat_history = state["chat_history"]
        if not hasattr(chat_history, "to_list"):
            raise NodeValidationError(
                "TransformTasksNode requires chat_history object with 'to_list' method"
            )

        # If tasks are provided, validate they have required methods
        if "tasks" in state and state["tasks"]:
            tasks = state["tasks"]
            if not hasattr(tasks, "ids"):
                raise NodeValidationError(
                    "TransformTasksNode requires tasks object with 'ids' property"
                )
            if not hasattr(tasks, "set_definition"):
                raise NodeValidationError(
                    "TransformTasksNode requires tasks object with 'set_definition' method"
                )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing logic."""
        # Get configs
        llm_config = self.get_config(LLMEndpointConfig, config)
        prompt_config = self.get_config(PromptConfig, config)

        # Get services through dependency injection
        llm_service = self.get_service(LLMService, llm_config)
        prompt_service = self.get_service(RAGPromptService)

        if not prompt_config.template_name:
            raise NodeValidationError(
                "TransformTasksNode requires 'template_name' attribute in config"
            )

        prompt = prompt_service.get_template(prompt_config.template_name)

        if "tasks" in state and state["tasks"]:
            tasks = state["tasks"]
        else:
            tasks = UserTasks([state["messages"][0].content])

        # Prepare the async tasks for all user tasks
        async_jobs = []
        for task_id in tasks.ids:
            msg = prompt.format(
                chat_history=state["chat_history"].to_list(),
                task=tasks(task_id).definition,
            )

            # Asynchronously invoke the model for each question
            async_jobs.append((llm_service.invoke(msg), task_id))

        # Gather all the responses asynchronously
        responses = (
            await asyncio.gather(*(jobs[0] for jobs in async_jobs))
            if async_jobs
            else []
        )
        task_ids = [jobs[1] for jobs in async_jobs] if async_jobs else []

        # Replace each question with its transformed version
        for response, task_id in zip(responses, task_ids, strict=False):
            tasks.set_definition(task_id, response.content)

        return {**state, "tasks": tasks}
