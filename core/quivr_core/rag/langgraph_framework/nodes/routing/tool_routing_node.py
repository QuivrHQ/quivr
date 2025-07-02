from typing import Optional, List
import asyncio
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from langgraph.types import Send
from quivr_core.rag.langgraph_framework.state import TasksCompletion
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.prompt.registry import get_prompt
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.utils import collect_tools, combine_documents
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node


@register_node(
    name="tool_routing",
    description="Route user tasks to appropriate tools based on task analysis",
    category="routing",
    version="1.0.0",
    dependencies=["llm_service"],
)
class ToolRoutingNode(BaseNode):
    """
    Node for routing user input to the correct tool.
    """

    NODE_NAME = "tool_routing"

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "tasks" not in state:
            raise NodeValidationError(
                "ToolRoutingNode requires 'tasks' attribute in state"
            )

        if not state["tasks"]:
            raise NodeValidationError(
                "ToolRoutingNode requires non-empty tasks in state"
            )

        # Validate tasks object has required methods
        tasks = state["tasks"]
        if not hasattr(tasks, "has_tasks"):
            raise NodeValidationError(
                "ToolRoutingNode requires tasks object with 'has_tasks' method"
            )

        if not hasattr(tasks, "ids"):
            raise NodeValidationError(
                "ToolRoutingNode requires tasks object with 'ids' property"
            )

        if "chat_history" not in state:
            raise NodeValidationError(
                "ToolRoutingNode requires 'chat_history' attribute in state"
            )

        # Validate chat_history has required methods
        chat_history = state["chat_history"]
        if not hasattr(chat_history, "to_list"):
            raise NodeValidationError(
                "ToolRoutingNode requires chat_history object with 'to_list' method"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing split logic."""
        # Get configs
        llm_config = self.get_config(LLMEndpointConfig, config)
        workflow_config = self.get_config(WorkflowConfig, config)

        # Get services through dependency injection
        llm_service = self.get_service(LLMService, llm_config)

        # Use prompt registry directly instead of prompt service
        prompt = get_prompt("tool_routing")

        tasks = state["tasks"]
        if not tasks.has_tasks():
            return [Send("generate_rag", state)]

        validated_tools, _ = collect_tools(workflow_config)

        async_jobs = []
        for task_id in tasks.ids:
            input = {
                "chat_history": state["chat_history"].to_list(),
                "tasks": tasks(task_id).definition,
                "context": combine_documents(tasks(task_id).docs),
                "activated_tools": validated_tools,
            }

            msg = prompt.format(**input)
            async_jobs.append(
                (
                    llm_service.invoke_with_structured_output(msg, TasksCompletion),
                    task_id,
                )
            )

        responses: List[TasksCompletion] = (
            await asyncio.gather(*(jobs[0] for jobs in async_jobs))
            if async_jobs
            else []
        )
        task_ids = [jobs[1] for jobs in async_jobs] if async_jobs else []

        for response, task_id in zip(responses, task_ids, strict=False):
            tasks.set_completion(task_id, response.is_task_completable)
            if not response.is_task_completable and response.tool:
                tasks.set_tool(task_id, response.tool)

        send_list: List[Send] = []
        payload = {**state, "tasks": tasks}

        if tasks.has_non_completable_tasks():
            send_list.append(Send("run_tool", payload))
        else:
            send_list.append(Send("generate_rag", payload))

        return send_list
