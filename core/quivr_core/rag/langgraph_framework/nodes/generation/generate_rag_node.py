from typing import Optional, Dict, Any, Tuple, List
from quivr_core.rag.langgraph_framework.nodes.base.base_node import (
    BaseNode,
    NodeValidationError,
)
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.entities.prompt import PromptConfig
from langchain_core.documents import Document

from quivr_core.rag.langgraph_framework.utils import reduce_rag_context
from quivr_core.rag.prompts import TemplatePromptName
from quivr_core.rag.utils import combine_documents

from quivr_core.rag.langgraph_framework.services.prompt_service import PromptService
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor


class GenerateRagNode(BaseNode):
    """
    Node for generating a response using a RAG model.
    """

    NODE_NAME = "generate_rag"
    CONFIG_TYPES = (WorkflowConfig, PromptConfig, LLMEndpointConfig)

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

    def get_config(
        self, config: Optional[Dict[str, Any]] = None
    ) -> Tuple[WorkflowConfig, PromptConfig, LLMEndpointConfig]:
        """Extract and validate the filter history and LLM configs."""
        if config is None or not self.config_extractor:
            return WorkflowConfig(), PromptConfig(), LLMEndpointConfig()

        workflow_dict, prompt_dict, llm_config_dict = self.config_extractor(config)

        return (
            WorkflowConfig.model_validate(workflow_dict),
            PromptConfig.model_validate(prompt_dict),
            LLMEndpointConfig.model_validate(llm_config_dict),
        )

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

    def _build_rag_prompt_inputs(
        self, state, prompt, docs: List[Document] | None
    ) -> Dict[str, Any]:
        """Build the input dictionary for RAG_ANSWER_PROMPT.

        Args:
            state: Current agent state
            docs: List of documents or None

        Returns:
            Dictionary containing all inputs needed for RAG_ANSWER_PROMPT
        """
        messages = state["messages"]
        user_task = messages[0].content
        files = state["files"]
        # available_tools, _ = collect_tools(self.retrieval_config.workflow_config)

        return {
            "context": combine_documents(docs) if docs else "None",
            "task": user_task,
            "rephrased_task": state["tasks"].definitions if state["tasks"] else "None",
            "custom_instructions": prompt if prompt else "None",
            "files": files if files else "None",
            "chat_history": state["chat_history"].to_list(),
            # "reasoning": state["reasoning"] if "reasoning" in state else "None",
            # "tools": available_tools,
        }

    async def execute(self, state, config: Optional[Dict[str, Any]] = None):
        # Get config using the injected extractor
        workflow_config, prompt_config, llm_config = self.get_config(config)

        custom_prompt = prompt_config.prompt

        tasks = state["tasks"]
        docs = tasks.docs if tasks else []
        inputs = self._build_rag_prompt_inputs(state, custom_prompt, docs)
        prompt = self.prompt_service.get_template(TemplatePromptName.RAG_ANSWER_PROMPT)
        state, inputs = reduce_rag_context(
            state,
            inputs,
            prompt,
            self.llm_service.count_tokens,
            llm_config.max_context_tokens,
        )
        msg = prompt.format(**inputs)
        llm = self.llm_service.bind_tools(self.name, workflow_config)
        response = llm.invoke(msg)

        return {**state, "messages": [response]}
