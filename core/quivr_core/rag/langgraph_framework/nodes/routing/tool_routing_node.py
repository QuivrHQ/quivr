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
from quivr_core.rag.langgraph_framework.services.prompt_service import PromptService
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.utils import collect_tools, combine_documents


class ToolRoutingNode(BaseNode):
    """
    Node for routing user input to the correct tool.
    """

    NODE_NAME = "tool_routing"
    CONFIG_TYPES = (PromptConfig,)

    def __init__(
        self,
        prompt_service: Optional[PromptService] = None,
        llm_service: Optional[LLMService] = None,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)

        self.prompt_service = prompt_service
        self._prompt_service_user_provided = prompt_service is not None

        self.llm_service = llm_service
        self._llm_service_user_provided = llm_service is not None

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        pass

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing split logic."""
        # Type-safe config extraction
        prompt_config, _ = self.get_config(PromptConfig, config)

        llm_config, llm_config_changed = self.get_config(LLMEndpointConfig, config)
        # Initialize LLMService if needed
        if not self.llm_service or (
            not self._llm_service_user_provided and llm_config_changed
        ):
            self.logger.debug(
                "Initializing/reinitializing LLMService due to config change"
            )
            self.llm_service = LLMService(llm_config=llm_config)
        assert self.llm_service

        workflow_config, _ = self.get_config(WorkflowConfig, config)

        if not self.prompt_service:
            self.prompt_service = PromptService()
        assert self.prompt_service

        prompt = self.prompt_service.get_template(
            TemplatePromptName.TOOL_ROUTING_PROMPT
        )

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
                    self.llm_service.invoke_with_structured_output(
                        msg, TasksCompletion
                    ),
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
