from typing import Optional
import asyncio
from quivr_core.rag.entities.config import LLMEndpointConfig
from quivr_core.rag.langgraph_framework.nodes.base.node import (
    BaseNode,
    NodeValidationError,
)
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.services.prompt_service import PromptService
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.task import UserTasks


class TransformTasksNode(BaseNode):
    """
    Node for routing user input to appropriate processing paths.
    """

    NODE_NAME = "transform_tasks"
    CONFIG_TYPES = (LLMEndpointConfig,)

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        prompt_service: Optional[PromptService] = None,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)

        self.llm_service = llm_service
        self._llm_service_user_provided = llm_service is not None

        self.prompt_service = prompt_service
        self._prompt_service_user_provided = prompt_service is not None

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        pass

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing logic."""

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

        # Initialize PromptService if needed
        if not self.prompt_service:
            self.logger.debug(
                "Initializing/reinitializing PromptService due to config change"
            )
            self.prompt_service = PromptService()
        assert self.prompt_service

        prompt_config, _ = self.get_config(PromptConfig, config)

        if not prompt_config.template_name:
            raise NodeValidationError(
                "TransformTasksNode requires 'template_name' attribute in config"
            )

        prompt = self.prompt_service.get_template(prompt_config.template_name)

        if "tasks" in state and state["tasks"]:
            tasks = state["tasks"]
        else:
            tasks = UserTasks([state["messages"][0].content])

        # Prepare the async tasks for all user tsks
        async_jobs = []
        for task_id in tasks.ids:
            msg = prompt.format(
                chat_history=state["chat_history"].to_list(),
                task=tasks(task_id).definition,
            )

            # Asynchronously invoke the model for each question
            async_jobs.append(
                (
                    self.llm_service.invoke(msg),
                    task_id,
                )
            )

        # Gather all the responses asynchronously
        responses = (
            await asyncio.gather(*(jobs[0] for jobs in async_jobs))
            if async_jobs
            else []
        )
        task_ids = [jobs[1] for jobs in async_jobs] if async_jobs else []

        # Replace each question with its condensed version
        for response, task_id in zip(responses, task_ids, strict=False):
            tasks.set_definition(task_id, response.content)

        return {**state, "tasks": tasks}
