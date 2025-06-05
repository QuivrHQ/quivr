from typing import Optional, Dict, Any, List
from quivr_core.rag.langgraph_framework.nodes.base.base_node import (
    BaseNode,
    NodeValidationError,
)
from langchain_core.prompts import BasePromptTemplate
from langchain_core.documents import Document
from datetime import datetime
from quivr_core.rag.utils import format_dict
from quivr_core.rag.entities.config import WorkflowConfig

from quivr_core.rag.prompts import TemplatePromptName


from quivr_core.rag.langgraph_framework.services.prompt_service import PromptService
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor


class GenerateZendeskRagNode(BaseNode):
    """
    Node for generating a response using a Zendesk RAG model.
    """

    NODE_NAME = "generate_zendesk_rag"
    CONFIG_TYPES = (WorkflowConfig,)

    def __init__(
        self,
        prompt_service: PromptService,
        llm_service: LLMService,
        config_extractor: ConfigExtractor,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)
        self.prompt_service = prompt_service
        self.llm_service = llm_service

    def get_config(self, config: Optional[Dict[str, Any]] = None) -> WorkflowConfig:
        """Extract and validate the filter history and LLM configs."""
        if config is None or not self.config_extractor:
            return WorkflowConfig()

        workflow_dict = self.config_extractor(config)

        return WorkflowConfig.model_validate(workflow_dict)

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

        if "tasks" not in state:
            raise NodeValidationError(
                "RetrieveNode requires 'tasks' attribute in state"
            )

        if not state["tasks"]:
            raise NodeValidationError("RetrieveNode requires non-empty tasks in state")

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[Dict[str, Any]] = None):
        # Get config using the injected extractor
        workflow_config = self.get_config(config)

        tasks = state["tasks"]
        docs: List[Document] = tasks.docs if tasks else []
        messages = state["messages"]
        user_task = messages[0].content

        prompt_template: BasePromptTemplate = self.prompt_service.get_template(
            TemplatePromptName.ZENDESK_TEMPLATE_PROMPT
        )

        ticket_metadata = state["ticket_metadata"] or {}
        user_metadata = state["user_metadata"] or {}
        ticket_history = state.get("ticket_history", "")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        inputs = {
            "similar_tickets": "\n".join([doc.page_content for doc in docs]),
            "ticket_metadata": format_dict(ticket_metadata),
            "user_metadata": format_dict(user_metadata),
            "client_query": user_task,
            "ticket_history": ticket_history,
            "current_time": current_time,
        }

        required_variables = prompt_template.input_variables
        for variable in required_variables:
            if variable not in inputs:
                inputs[variable] = state.get(variable, "")

        msg = prompt_template.format_prompt(**inputs)
        llm = self.llm_service.bind_tools(self.name, workflow_config)

        response = llm.invoke(msg)

        return {**state, "messages": [response]}
