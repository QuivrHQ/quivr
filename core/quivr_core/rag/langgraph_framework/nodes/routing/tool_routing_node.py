from typing import Optional, List
import asyncio
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.langgraph_framework.nodes.base.node import (
    BaseNode,
)
from langgraph.types import Send
from quivr_core.rag.langgraph_framework.state import TasksCompletion
from quivr_core.rag.prompts import TemplatePromptName
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.services.rag_prompt_service import (
    RAGPromptService,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.utils import collect_tools, combine_documents
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node


@register_node(
    name="tool_routing",
    description="Route user tasks to appropriate tools based on task analysis",
    category="routing",
    version="1.0.0",
    dependencies=["llm_service", "prompt_service"],
)
class ToolRoutingNode(BaseNode):
    """
    Node for routing user input to the correct tool.
    """

    NODE_NAME = "tool_routing"
    CONFIG_TYPES = (PromptConfig, LLMEndpointConfig, WorkflowConfig)

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        pass

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing split logic."""
        # Get configs
        prompt_config, _ = self.get_config(PromptConfig, config)
        llm_config, _ = self.get_config(LLMEndpointConfig, config)
        workflow_config, _ = self.get_config(WorkflowConfig, config)

        # Get services through dependency injection
        llm_service = self.get_service(LLMService, llm_config)
        prompt_service = self.get_service(RAGPromptService, None)  # Uses default config

        prompt = prompt_service.get_template(TemplatePromptName.TOOL_ROUTING_PROMPT)

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
