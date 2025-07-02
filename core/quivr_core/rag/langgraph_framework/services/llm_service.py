import logging
import openai
from typing import Any, Type, List, Dict, Optional, TYPE_CHECKING
from langchain_core.tools import BaseTool as LangChainBaseTool
from langchain_core.runnables import Runnable
from quivr_core.llm import LLMEndpoint
from quivr_core.rag.entities.config import LLMEndpointConfig, NodeConfig
from pydantic import BaseModel

if TYPE_CHECKING:
    from quivr_core.rag.langgraph_framework.services.tool_service import (
        ToolService,
        ToolCallTracker,
    )
    from quivr_core.llm_tools.base.tool import QuivrBaseTool

logger = logging.getLogger("quivr_core")


class LLMService:
    """Service for LLM operations including structured output, token counting, and tool binding."""

    def __init__(
        self,
        llm_config: LLMEndpointConfig,
        tool_service: Optional["ToolService"] = None,
    ):
        self.config = llm_config
        self.llm_endpoint = LLMEndpoint.from_config(llm_config)
        self.tool_service = tool_service

    async def invoke(self, prompt: str) -> Any:
        """
        Invoke the LLM with the given prompt.

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            The response from the LLM
        """
        return await self.llm_endpoint._llm.ainvoke(prompt)

    async def invoke_with_tools(
        self, prompt: str, tool_enabled_llm: Runnable, **kwargs
    ) -> Any:
        """
        Invoke a tool-enabled LLM with the given prompt.

        Args:
            prompt: The prompt to send to the LLM
            tool_enabled_llm: LLM instance with tools bound
            **kwargs: Additional arguments to pass to the LLM

        Returns:
            The response from the LLM, potentially including tool calls
        """
        try:
            return await tool_enabled_llm.ainvoke(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Error invoking tool-enabled LLM: {e}")
            raise

    def invoke_with_tools_sync(
        self, prompt: str, tool_enabled_llm: Runnable, **kwargs
    ) -> Any:
        """
        Synchronous version of invoke_with_tools.

        Args:
            prompt: The prompt to send to the LLM
            tool_enabled_llm: LLM instance with tools bound
            **kwargs: Additional arguments to pass to the LLM

        Returns:
            The response from the LLM, potentially including tool calls
        """
        try:
            return tool_enabled_llm.invoke(prompt, **kwargs)
        except Exception as e:
            logger.error(f"Error invoking tool-enabled LLM (sync): {e}")
            raise

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

    def bind_tools_to_llm(
        self,
        langchain_tools: List[LangChainBaseTool],
        tool_choice: Optional[str] = None,
    ) -> Runnable:
        """
        Bind tools to the LLM if function calling is supported.

        Args:
            langchain_tools: List of LangChain tools to bind
            tool_choice: Tool choice strategy ("auto", "any", specific tool name, or None)

        Returns:
            LLM instance with tools bound, or base LLM if no tools/function calling
        """
        if not langchain_tools:
            return self.llm_endpoint._llm

        if not self.supports_function_calling():
            logger.warning("LLM does not support function calling, returning base LLM")
            return self.llm_endpoint._llm

        try:
            # Most modern LLMs support bind_tools method
            if hasattr(self.llm_endpoint._llm, "bind_tools"):
                if tool_choice:
                    return self.llm_endpoint._llm.bind_tools(
                        langchain_tools, tool_choice=tool_choice
                    )
                else:
                    return self.llm_endpoint._llm.bind_tools(langchain_tools)
            else:
                logger.error("LLM does not support tool binding method")
                raise ValueError("LLM does not support tool binding method")
        except Exception as e:
            logger.error(f"Failed to bind tools to LLM: {e}")
            raise e

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

    def extract_tool_calls_from_response(self, response: Any) -> List[Dict[str, Any]]:
        """
        Extract tool calls from LLM response.

        Args:
            response: LLM response that may contain tool calls

        Returns:
            List of tool call dictionaries with 'name' and 'args' keys
        """
        tool_calls = []

        # Check if response has tool_calls attribute (common in OpenAI-style responses)
        if hasattr(response, "tool_calls") and response.tool_calls:
            for tool_call in response.tool_calls:
                if isinstance(tool_call, dict):
                    tool_calls.append(
                        {
                            "name": tool_call.get("name", "unknown"),
                            "args": tool_call.get("args", {}),
                            "id": tool_call.get("id", None),
                        }
                    )
                else:
                    # Handle other tool call formats
                    tool_calls.append(
                        {
                            "name": getattr(tool_call, "name", "unknown"),
                            "args": getattr(tool_call, "args", {}),
                            "id": getattr(tool_call, "id", None),
                        }
                    )

        # Check if response has additional_kwargs with tool_calls (alternative format)
        elif (
            hasattr(response, "additional_kwargs")
            and "tool_calls" in response.additional_kwargs
        ):
            for tool_call in response.additional_kwargs["tool_calls"]:
                if "function" in tool_call:
                    func_call = tool_call["function"]
                    # Handle arguments that might be string or dict
                    args = func_call.get("arguments", {})
                    if isinstance(args, str):
                        try:
                            import json

                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}

                    tool_calls.append(
                        {
                            "name": func_call.get("name", "unknown"),
                            "args": args,
                            "id": tool_call.get("id", None),
                        }
                    )

        return tool_calls

    def has_tool_calls(self, response: Any) -> bool:
        """
        Check if LLM response contains tool calls.

        Args:
            response: LLM response to check

        Returns:
            True if response contains tool calls, False otherwise
        """
        return len(self.extract_tool_calls_from_response(response)) > 0

    async def invoke_for_node(
        self,
        prompt: str,
        node_config: Optional[NodeConfig] = None,
        tool_choice: Optional[str] = None,
        output_class: Optional[Type[BaseModel]] = None,
        **llm_kwargs,
    ) -> Dict[str, Any]:
        """
        Unified invoke method that automatically handles tools and structured output.

        Args:
            prompt: Prompt to send to the LLM
            node_config: Optional node configuration containing tool definitions
            tool_choice: Tool choice strategy for LLM
            output_class: Optional Pydantic model class for structured output
            **llm_kwargs: Additional arguments to pass to LLM

        Returns:
            Dictionary containing response, tool calls summary (if tools used), and execution status
        """
        # Check if we need structured output
        has_tools = node_config and node_config.tools_config and self.tool_service

        # If no tools, decide between regular invoke and structured output
        if not has_tools:
            if output_class:
                response = await self.invoke_with_structured_output(
                    prompt, output_class
                )
            else:
                response = await self.invoke(prompt)

            return {
                "response": response,
                "tool_calls_summary": None,
                "success": True,
                "tools_used": 0,
                "structured_output": output_class is not None,
                "function_calling_supported": self.supports_function_calling(),
            }

        try:
            # Step 1: Prepare tools using ToolService
            # We already know tool_service and node_config are not None from the check above
            assert self.tool_service is not None
            assert node_config is not None

            tool_setup = self.tool_service.prepare_tools_for_node()

            if not tool_setup["success"]:
                return {
                    "response": None,
                    "tool_calls_summary": None,
                    "success": False,
                    "error": f"Tool preparation failed: {tool_setup.get('error', 'Unknown error')}",
                }

            quivr_tools = tool_setup["quivr_tools"]
            langchain_tools = tool_setup["langchain_tools"]
            tracker = tool_setup["tracker"]

            # Step 2: Handle the combination of tools and structured output
            if output_class and langchain_tools:
                # Tools and structured output together is complex
                # First execute with tools, then try to parse structured output if needed
                logger.warning(
                    "Using both tools and structured output. Structured output may not work as expected with tool calls."
                )

            # Step 3: Bind tools to LLM
            tool_enabled_llm = self.bind_tools_to_llm(langchain_tools, tool_choice)

            # Step 4: Execute LLM with tools
            if output_class and not langchain_tools:
                # Only structured output, no tools
                response = await self.invoke_with_structured_output(
                    prompt, output_class
                )
            else:
                # Tools present (with or without structured output)
                response = await self.invoke_with_tools(
                    prompt, tool_enabled_llm, **llm_kwargs
                )

            # Step 5: Process any tool calls
            if langchain_tools:
                await self._process_tool_calls_internal(response, quivr_tools, tracker)

            return {
                "response": response,
                "tool_calls_summary": tracker.get_calls_summary()
                if langchain_tools
                else None,
                "success": True,
                "tools_used": len(quivr_tools),
                "structured_output": output_class is not None,
                "function_calling_supported": self.supports_function_calling(),
            }

        except Exception as e:
            logger.error(f"Error executing node with tools: {e}")
            return {
                "response": None,
                "tool_calls_summary": None,
                "success": False,
                "error": str(e),
            }

    def invoke_for_node_sync(
        self,
        prompt: str,
        node_config: Optional[NodeConfig] = None,
        tool_choice: Optional[str] = None,
        output_class: Optional[Type[BaseModel]] = None,
        **llm_kwargs,
    ) -> Dict[str, Any]:
        """
        Synchronous version of invoke_for_node.

        Args:
            prompt: Prompt to send to the LLM
            node_config: Optional node configuration containing tool definitions
            tool_choice: Tool choice strategy for LLM
            output_class: Optional Pydantic model class for structured output
            **llm_kwargs: Additional arguments to pass to LLM

        Returns:
            Dictionary containing response, tool calls summary (if tools used), and execution status
        """
        # Check if we need structured output
        has_tools = node_config and node_config.tools_config and self.tool_service

        # If no tools, decide between regular invoke and structured output
        if not has_tools:
            if output_class:
                response = self.invoke_with_structured_output_sync(prompt, output_class)
            else:
                response = self.llm_endpoint._llm.invoke(prompt)

            return {
                "response": response,
                "tool_calls_summary": None,
                "success": True,
                "tools_used": 0,
                "structured_output": output_class is not None,
                "function_calling_supported": self.supports_function_calling(),
            }

        try:
            # Step 1: Prepare tools using ToolService
            # We already know tool_service and node_config are not None from the check above
            assert self.tool_service is not None
            assert node_config is not None

            tool_setup = self.tool_service.prepare_tools_for_node()

            if not tool_setup["success"]:
                return {
                    "response": None,
                    "tool_calls_summary": None,
                    "success": False,
                    "error": f"Tool preparation failed: {tool_setup.get('error', 'Unknown error')}",
                }

            langchain_tools = tool_setup["langchain_tools"]

            # Step 2: Handle the combination of tools and structured output
            if output_class and langchain_tools:
                logger.warning(
                    "Using both tools and structured output in sync mode. Structured output may not work as expected with tool calls."
                )

            # Step 3: Bind tools to LLM
            tool_enabled_llm = self.bind_tools_to_llm(langchain_tools, tool_choice)

            # Step 4: Execute LLM with tools (sync)
            if output_class and not langchain_tools:
                # Only structured output, no tools
                response = self.invoke_with_structured_output_sync(prompt, output_class)
            else:
                # Tools present (with or without structured output)
                response = self.invoke_with_tools_sync(
                    prompt, tool_enabled_llm, **llm_kwargs
                )

            # Note: For sync version, we don't process tool calls automatically
            # since tool execution is async. The caller would need to handle tool calls.

            return {
                "response": response,
                "tool_calls_summary": None,
                "success": True,
                "tools_used": len(tool_setup["quivr_tools"]),
                "structured_output": output_class is not None,
                "function_calling_supported": self.supports_function_calling(),
                "note": "Tool calls in response need to be processed separately for sync version"
                if langchain_tools
                else None,
            }

        except Exception as e:
            logger.error(f"Error executing node with tools (sync): {e}")
            return {
                "response": None,
                "tool_calls_summary": None,
                "success": False,
                "error": str(e),
            }

    async def _process_tool_calls_internal(
        self, response: Any, tools: List["QuivrBaseTool"], tracker: "ToolCallTracker"
    ) -> None:
        """Internal method to process tool calls from LLM response."""
        if not self.tool_service:
            logger.warning("No ToolService available for processing tool calls")
            return

        tool_calls = self.extract_tool_calls_from_response(response)

        for tool_call in tool_calls:
            if not tracker.can_make_call():
                logger.warning(f"Maximum tool calls ({tracker.max_tool_calls}) reached")
                break

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Execute tool using ToolService
            result = await self.tool_service.execute_tool_by_name(
                tool_name, tool_args, tools, tracker
            )

            if not result["success"]:
                logger.warning(
                    f"Tool execution failed for '{tool_name}': {result.get('error')}"
                )

    def set_tool_service(self, tool_service: "ToolService") -> None:
        """
        Set the ToolService instance for this LLMService.

        Args:
            tool_service: ToolService instance to use for tool operations
        """
        self.tool_service = tool_service

    def has_tool_service(self) -> bool:
        """
        Check if this LLMService has a ToolService configured.

        Returns:
            True if ToolService is available, False otherwise
        """
        return self.tool_service is not None
