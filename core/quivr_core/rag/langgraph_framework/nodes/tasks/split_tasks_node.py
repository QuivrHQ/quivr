from typing import Optional, List
import asyncio
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.entities.routing_entity import SplittedInput
from quivr_core.rag.prompt.registry import get_prompt
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.services.tool_service import ToolService
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node
import logging

logger = logging.getLogger("quivr_core")


@register_node(
    name="split_tasks",
    description="Split user input into multiple processing paths",
    category="tasks",
    version="1.0.0",
    dependencies=["llm_service", "tool_service"],
)
class SplitTasksNode(BaseNode):
    """
    Node for transforming user tasks.
    """

    NODE_NAME = "split_tasks"

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        # Validate messages (used for fallback task creation)
        if "messages" not in state:
            raise NodeValidationError(
                "SplitTasksNode requires 'messages' attribute in state"
            )

        if not state["messages"]:
            raise NodeValidationError(
                "SplitTasksNode requires non-empty messages in state"
            )

        # Validate chat_history
        if "chat_history" not in state:
            raise NodeValidationError(
                "SplitTasksNode requires 'chat_history' attribute in state"
            )

        # Validate chat_history has required methods
        chat_history = state["chat_history"]
        if not hasattr(chat_history, "to_list"):
            raise NodeValidationError(
                "SplitTasksNode requires chat_history object with 'to_list' method"
            )

        # If tasks are provided, validate they have required methods
        if "tasks" in state and state["tasks"]:
            tasks = state["tasks"]
            if not hasattr(tasks, "ids"):
                raise NodeValidationError(
                    "SplitTasksNode requires tasks object with 'ids' property"
                )
            if not hasattr(tasks, "set_definition"):
                raise NodeValidationError(
                    "SplitTasksNode requires tasks object with 'set_definition' method"
                )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing logic with enhanced LLMService."""
        # Get configs
        workflow_config = self.get_config(WorkflowConfig, config)
        llm_config = self.get_config(LLMEndpointConfig, config)
        prompt_config = self.get_config(PromptConfig, config)

        node_config = workflow_config.get_node_config_by_name(self.name)

        # Get services through dependency injection (though this node typically doesn't use tools)
        tool_service = self.get_service(ToolService, node_config.tools_config)

        llm_service = self.get_service(LLMService, llm_config)
        llm_service.set_tool_service(tool_service)

        if not prompt_config.template_name:
            raise NodeValidationError(
                "SplitTasksNode requires 'template_name' attribute in config"
            )

        # Use prompt registry directly instead of prompt service
        # Convert enum to string for registry lookup
        template_name = (
            prompt_config.template_name.value
            if hasattr(prompt_config.template_name, "value")
            else str(prompt_config.template_name)
        )
        prompt = get_prompt(template_name)

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
            # Use the new unified method for potential future tool support
            async_jobs.append(
                (
                    llm_service.invoke_for_node(
                        prompt=msg, node_config=node_config, output_class=SplittedInput
                    ),
                    task_id,
                )
            )

        # Gather all the responses asynchronously
        raw_responses = (
            await asyncio.gather(*(jobs[0] for jobs in async_jobs))
            if async_jobs
            else []
        )

        # Extract the actual responses from the result dicts
        responses: List[SplittedInput] = []
        for result in raw_responses:
            if result["success"]:
                responses.append(result["response"])
            else:
                logger.error(
                    f"Task splitting failed: {result.get('error', 'Unknown error')}"
                )
                # Continue with other responses

        # Replace each question with its condensed version
        _tasks: UserTasks = UserTasks()
        for response in responses:
            _tasks.add_tasks(response.task_list or [])

        return {**state, "tasks": _tasks}
