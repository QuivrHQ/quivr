from typing import Optional, Dict, Any, List
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.entities.config import (
    LLMEndpointConfig,
    WorkflowConfig,
)
from quivr_core.rag.entities.prompt import PromptConfig
from langchain_core.documents import Document

from quivr_core.rag.langgraph_framework.utils import reduce_rag_context
from quivr_core.rag.utils import combine_documents
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.prompt.registry import get_prompt
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.services.tool_service import ToolService
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node


@register_node(
    name="generate_rag",
    description="Generate RAG responses using retrieved documents and LLM",
    category="generation",
    version="1.0.0",
    dependencies=["llm_service", "tool_service"],
)
class GenerateRagNode(BaseNode):
    """
    Node for generating a response using a RAG model.
    """

    NODE_NAME = "generate_rag"

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "messages" not in state:
            raise NodeValidationError(
                "GenerateRagNode requires 'messages' attribute in state"
            )

        if not state["messages"]:
            raise NodeValidationError(
                "GenerateRagNode requires non-empty messages in state"
            )

        if "tasks" not in state:
            raise NodeValidationError(
                "GenerateRagNode requires 'tasks' attribute in state"
            )

        if not state["tasks"]:
            raise NodeValidationError(
                "GenerateRagNode requires non-empty tasks in state"
            )

        # Validate files
        if "files" not in state:
            raise NodeValidationError(
                "GenerateRagNode requires 'files' attribute in state"
            )

        # Validate chat_history
        if "chat_history" not in state:
            raise NodeValidationError(
                "GenerateRagNode requires 'chat_history' attribute in state"
            )

        # Validate chat_history has required methods
        chat_history = state["chat_history"]
        if not hasattr(chat_history, "to_list"):
            raise NodeValidationError(
                "GenerateRagNode requires chat_history object with 'to_list' method"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    def _build_rag_prompt_inputs(
        self, state, prompt, docs: List[Document] | None
    ) -> Dict[str, Any]:
        """Build the input dictionary for RAG_ANSWER_PROMPT."""
        messages = state["messages"]
        user_task = messages[0].content
        files = state["files"]

        return {
            "context": combine_documents(docs) if docs else "None",
            "task": user_task,
            "rephrased_task": state["tasks"].definitions if state["tasks"] else "None",
            "custom_instructions": prompt if prompt else "None",
            "files": files if files else "None",
            "chat_history": state["chat_history"].to_list(),
        }

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute RAG generation with new unified LLMService and tool support."""
        # Get configs
        workflow_config = self.get_config(WorkflowConfig, config)
        prompt_config = self.get_config(PromptConfig, config)
        llm_config = self.get_config(LLMEndpointConfig, config)

        node_config = workflow_config.get_node_config_by_name(self.name)
        assert node_config is not None, "Node config not found"

        # Get services through dependency injection
        tool_service = self.get_service(ToolService, node_config.tools_config)

        llm_service = self.get_service(LLMService, llm_config)
        llm_service.set_tool_service(tool_service)

        custom_prompt = prompt_config.prompt
        tasks = state["tasks"]
        docs = tasks.docs if tasks else []
        inputs = self._build_rag_prompt_inputs(state, custom_prompt, docs)

        prompt = get_prompt("rag_answer")

        state, inputs = reduce_rag_context(
            state,
            inputs,
            prompt,
            llm_service.count_tokens,
            llm_config.max_context_tokens,
        )

        msg = prompt.format(**inputs)

        # Use the new unified invoke_for_node method
        result = await llm_service.invoke_for_node(
            prompt=msg,
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
