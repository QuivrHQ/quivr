from typing import Optional, List
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from langchain_core.prompts import BasePromptTemplate
from langchain_core.documents import Document
from datetime import datetime
from quivr_core.rag.utils import format_dict
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.prompts import TemplatePromptName
from quivr_core.rag.langgraph_framework.services.rag_prompt_service import (
    RAGPromptService,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node


@register_node(
    name="generate_zendesk_rag",
    description="Generate Zendesk-specific RAG responses with ticket context and metadata",
    category="generation",
    version="1.0.0",
    dependencies=["llm_service", "prompt_service"],
)
class GenerateZendeskRagNode(BaseNode):
    """
    Node for generating a response using a Zendesk RAG model.
    """

    NODE_NAME = "generate_zendesk_rag"

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "messages" not in state:
            raise NodeValidationError(
                "GenerateZendeskRagNode requires 'messages' attribute in state"
            )
        if not state["messages"]:
            raise NodeValidationError(
                "GenerateZendeskRagNode requires non-empty messages in state"
            )
        if "tasks" not in state:
            raise NodeValidationError(
                "GenerateZendeskRagNode requires 'tasks' attribute in state"
            )
        if not state["tasks"]:
            raise NodeValidationError(
                "GenerateZendeskRagNode requires non-empty tasks in state"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute Zendesk RAG generation."""
        # Get configs
        workflow_config = self.get_config(WorkflowConfig, config)
        llm_config = self.get_config(LLMEndpointConfig, config)

        # Get services through dependency injection
        llm_service = self.get_service(LLMService, llm_config)
        prompt_service = self.get_service(RAGPromptService, None)  # Uses default config

        tasks = state["tasks"]
        docs: List[Document] = tasks.deduplicated_docs if tasks else []
        messages = state["messages"]
        user_task = messages[0].content

        prompt_template: BasePromptTemplate = prompt_service.get_template(
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
        llm = llm_service.bind_tools(self.name, workflow_config)

        response = llm.invoke(msg)

        return {**state, "messages": [response]}
