from typing import Optional, Dict, Any, List
from quivr_core.rag.langgraph_framework.nodes.base.node import (
    BaseNode,
    NodeValidationError,
)
from quivr_core.rag.entities.config import (
    LLMEndpointConfig,
    WorkflowConfig,
    RetrievalConfig,
)
from quivr_core.rag.entities.prompt import PromptConfig
from langchain_core.documents import Document

from quivr_core.rag.langgraph_framework.utils import reduce_rag_context
from quivr_core.rag.prompts import TemplatePromptName
from quivr_core.rag.utils import combine_documents
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.services.prompt_service import PromptService
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor


class GenerateRagNode(BaseNode):
    """
    Node for generating a response using a RAG model.
    """

    NODE_NAME = "generate_rag"
    CONFIG_TYPES = (WorkflowConfig, PromptConfig, LLMEndpointConfig, RetrievalConfig)

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
        """Execute RAG generation."""
        # Get configs with change detection
        workflow_config, _ = self.get_config(WorkflowConfig, config)
        prompt_config, _ = self.get_config(PromptConfig, config)
        retrieval_config, retrieval_config_changed = self.get_config(
            RetrievalConfig, config
        )

        # Initialize PromptService if needed
        if not self.prompt_service or (
            not self._prompt_service_user_provided and retrieval_config_changed
        ):
            self.logger.debug(
                "Initializing/reinitializing PromptService due to config change"
            )
            self.prompt_service = PromptService(retrieval_config=retrieval_config)
        assert self.prompt_service

        # Initialize LLMService if needed
        llm_config, llm_config_changed = self.get_config(LLMEndpointConfig, config)
        if not self.llm_service or (
            not self._llm_service_user_provided and llm_config_changed
        ):
            self.logger.debug(
                "Initializing/reinitializing LLMService due to config change"
            )
            self.llm_service = LLMService(llm_config=llm_config)
        assert self.llm_service

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
