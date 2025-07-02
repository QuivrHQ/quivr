from typing import Optional, List
from quivr_core.rag.entities.prompt import PromptConfig
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
from quivr_core.rag.prompt.registry import get_prompt
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.services.tool_service import ToolService
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node
from logging import getLogger

logger = getLogger(__name__)


@register_node(
    name="generate_zendesk_rag",
    description="Generate Zendesk-specific RAG responses with ticket context and metadata",
    category="generation",
    version="1.0.0",
    dependencies=["llm_service"],
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

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute Zendesk RAG generation using new unified LLMService."""
        # Get configs
        workflow_config = self.get_config(WorkflowConfig, config)
        llm_config = self.get_config(LLMEndpointConfig, config)

        node_config = workflow_config.get_node_config_by_name(self.name)

        # Extract workspace_id and zendesk_id from state or config
        workspace_id = state.get("workspace_id")

        if not workspace_id:
            raise ValueError("workspace_id must be provided in state for Zendesk tools")

        # Get services with runtime context - the ToolService will automatically
        # extract the right runtime args for each tool based on their schemas
        tool_service = self.get_service(
            ToolService,
            node_config.tools_config,
            runtime_context={"workspace_id": workspace_id},
        )
        llm_service = self.get_service(LLMService, llm_config)

        # Set the tool service on the LLM service
        llm_service.set_tool_service(tool_service)

        tasks = state["tasks"] if "tasks" in state else None
        docs: List[Document] = tasks.deduplicated_docs if tasks else []
        messages = state["messages"]
        user_task = messages[0].content

        prompt_config = self.get_config(PromptConfig, config)
        prompt_template: BasePromptTemplate
        if prompt_config.template_name:
            prompt_template = get_prompt(prompt_config.template_name)
        else:
            prompt_template = get_prompt("zendesk_template")

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

        # Use the new unified invoke_for_node method
        result = await llm_service.invoke_for_node(
            prompt=str(msg),
            node_config=node_config,
        )

        if not result["success"]:
            raise RuntimeError(
                f"LLM execution failed: {result.get('error', 'Unknown error')}"
            )

        response = result["response"]

        # Add tool call information to state if tools were used
        updated_state = {**state, "messages": [response]}
        if result["tool_calls_summary"]:
            updated_state["tool_calls_summary"] = result["tool_calls_summary"]
            updated_state["tools_used"] = result["tools_used"]

        return updated_state
