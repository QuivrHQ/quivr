import logging
import openai
from typing import Any, Type
from quivr_core.llm import LLMEndpoint
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from pydantic import BaseModel

logger = logging.getLogger("quivr_core")


class LLMService:
    """Service for LLM operations including structured output, token counting, and tool binding."""

    def __init__(self, llm_config: LLMEndpointConfig):
        self.config = llm_config
        self.llm_endpoint = LLMEndpoint.from_config(llm_config)

    async def invoke(self, prompt: str) -> Any:
        """
        Invoke the LLM with the given prompt.

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            The response from the LLM
        """
        return await self.llm_endpoint._llm.ainvoke(prompt)

    async def invoke_with_structured_output(
        self, prompt: str, output_class: Type[BaseModel]
    ) -> Any:
        """
        Invoke LLM with structured output, handling fallback for different methods.

        Args:
            prompt: The prompt to send to the LLM
            output_class: Pydantic model class for structured output

        Returns:
            Instance of output_class with the LLM's structured response
        """
        try:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                output_class, method="json_schema"
            )
            return await structured_llm.ainvoke(prompt)
        except openai.BadRequestError:
            logger.warning(
                "JSON schema method failed, falling back to default structured output"
            )
            structured_llm = self.llm_endpoint._llm.with_structured_output(output_class)
            return await structured_llm.ainvoke(prompt)

    def invoke_with_structured_output_sync(
        self, prompt: str, output_class: Type[BaseModel]
    ) -> Any:
        """
        Synchronous version of invoke_with_structured_output.

        Args:
            prompt: The prompt to send to the LLM
            output_class: Pydantic model class for structured output

        Returns:
            Instance of output_class with the LLM's structured response
        """
        try:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                output_class, method="json_schema"
            )
            return structured_llm.invoke(prompt)
        except openai.BadRequestError:
            logger.warning(
                "JSON schema method failed, falling back to default structured output"
            )
            structured_llm = self.llm_endpoint._llm.with_structured_output(output_class)
            return structured_llm.invoke(prompt)

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in the given text using the LLM endpoint's tokenizer.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens in the text
        """
        return self.llm_endpoint.count_tokens(text)

    def bind_tools(self, node_name: str, workflow_config: WorkflowConfig):
        """
        Bind tools to the LLM if function calling is supported and tools are available.

        Args:
            node_name: Name of the node to get tools for
            workflow_config: Workflow configuration containing tool definitions

        Returns:
            LLM instance with tools bound, or base LLM if no tools/function calling
        """
        if self.llm_endpoint.supports_func_calling():
            tools = workflow_config.get_node_tools(node_name)
            if tools:  # Only bind tools if there are any available
                return self.llm_endpoint._llm.bind_tools(tools, tool_choice="any")
        return self.llm_endpoint._llm

    def get_base_llm(self):
        """
        Get the base LLM instance without any tool binding.

        Returns:
            Base LLM instance
        """
        return self.llm_endpoint._llm

    def supports_function_calling(self) -> bool:
        """
        Check if the LLM supports function calling.

        Returns:
            True if function calling is supported, False otherwise
        """
        return self.llm_endpoint.supports_func_calling()

    def get_max_context_tokens(self) -> int:
        """
        Get the maximum context tokens for this LLM configuration.

        Returns:
            Maximum context tokens
        """
        return self.config.max_context_tokens

    def get_max_output_tokens(self) -> int:
        """
        Get the maximum output tokens for this LLM configuration.

        Returns:
            Maximum output tokens
        """
        return self.config.max_output_tokens
