from typing import Any, Optional, Dict
from quivr_core.llm_tools.llm_tools import LLMToolFactory
import asyncio
from quivr_core.rag.langgraph_framework.base.node import BaseNode
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node


@register_node(
    name="run_tool",
    description="Execute tools for tasks that require external tool invocation",
    category="tools",
    version="1.0.0",
    dependencies=["llm_tools"],
)
class RunToolNode(BaseNode):
    """
    Node for running a tool.
    """

    NODE_NAME = "run_tool"

    def __init__(
        self,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "tasks" not in state:
            raise NodeValidationError("RunToolNode requires 'tasks' attribute in state")

        if not state["tasks"]:
            raise NodeValidationError("RunToolNode requires non-empty tasks in state")

        # Validate tasks object has required methods
        tasks = state["tasks"]
        if not hasattr(tasks, "has_tasks"):
            raise NodeValidationError(
                "RunToolNode requires tasks object with 'has_tasks' method"
            )

        if not hasattr(tasks, "ids"):
            raise NodeValidationError(
                "RunToolNode requires tasks object with 'ids' property"
            )

        if not hasattr(tasks, "set_docs"):
            raise NodeValidationError(
                "RunToolNode requires tasks object with 'set_docs' method"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing logic."""
        tasks = state["tasks"]
        if not tasks.has_tasks():
            return {**state}

        # Prepare the async tasks for all questions
        async_jobs = []
        tool_wrappers: Dict[str, Any] = {}

        for task_id in tasks.ids:
            if not tasks(task_id).is_completable() and tasks(task_id).has_tool():
                tool = tasks(task_id).tool
                assert tool, "Tool is not set for task"
                tool_wrapper = LLMToolFactory.create_tool(tool, {})
                tool_wrappers[task_id] = tool_wrapper
                formatted_input = tool_wrapper.format_input(tasks(task_id).definition)
                async_jobs.append((tool_wrapper.tool.ainvoke(formatted_input), task_id))

        # Gather all the responses asynchronously
        responses = (
            await asyncio.gather(*(jobs[0] for jobs in async_jobs))
            if async_jobs
            else []
        )
        task_ids = [jobs[1] for jobs in async_jobs] if async_jobs else []

        for response, task_id in zip(responses, task_ids, strict=False):
            tool_wrapper = tool_wrappers[task_id]
            _docs = tool_wrapper.format_output(response)
            tasks.set_docs(task_id, _docs)

        return {**state, "tasks": tasks}
