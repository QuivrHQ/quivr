import logging
from typing import List, Optional, Dict, Any
from quivr_core.rag.entities.config import WorkflowConfig
from quivr_core.llm_tools.llm_tools import LLMToolFactory
from quivr_core.rag.utils import collect_tools

logger = logging.getLogger("quivr_core")


class ToolService:
    """Service for tool management and execution."""

    def __init__(self, workflow_config: WorkflowConfig):
        self.workflow_config = workflow_config

    def get_node_tools(self, node_name: str) -> List[Any]:
        """
        Get tools available for a specific node.

        Args:
            node_name: Name of the node

        Returns:
            List of tools available for the node
        """
        return self.workflow_config.get_node_tools(node_name)

    def get_activated_tools(self) -> List[Any]:
        """
        Get currently activated tools.

        Returns:
            List of activated tools
        """
        return self.workflow_config.activated_tools

    def get_validated_tools(self) -> List[Any]:
        """
        Get all validated tools.

        Returns:
            List of validated tools
        """
        return self.workflow_config.validated_tools

    def activate_tools(self, tool_names: List[str]):
        """
        Activate tools by name.

        Args:
            tool_names: List of tool names to activate
        """
        for tool_name in tool_names:
            for validated_tool in self.workflow_config.validated_tools:
                if tool_name == validated_tool.name:
                    if validated_tool not in self.workflow_config.activated_tools:
                        self.workflow_config.activated_tools.append(validated_tool)
                        logger.info(f"Activated tool: {tool_name}")

    def deactivate_tools(self, tool_names: List[str]):
        """
        Deactivate tools by name.

        Args:
            tool_names: List of tool names to deactivate
        """
        for tool_name in tool_names:
            tools_to_remove = [
                tool
                for tool in self.workflow_config.activated_tools
                if tool.name == tool_name
            ]
            for tool in tools_to_remove:
                self.workflow_config.activated_tools.remove(tool)
                logger.info(f"Deactivated tool: {tool_name}")

    def is_tool_activated(self, tool_name: str) -> bool:
        """
        Check if a tool is currently activated.

        Args:
            tool_name: Name of the tool to check

        Returns:
            True if tool is activated, False otherwise
        """
        return any(
            tool.name == tool_name for tool in self.workflow_config.activated_tools
        )

    def create_tool_instance(
        self, tool_name: str, config: Optional[Dict[str, Any]] = None
    ):
        """
        Create a tool instance by name.

        Args:
            tool_name: Name of the tool to create
            config: Optional configuration for the tool

        Returns:
            Tool instance

        Raises:
            ValueError: If tool is not found or not activated
        """
        if not self.is_tool_activated(tool_name):
            raise ValueError(f"Tool {tool_name} is not activated")

        return LLMToolFactory.create_tool(tool_name, config or {})

    async def execute_tool(
        self, tool_name: str, input_data: str, config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute a tool with given input.

        Args:
            tool_name: Name of the tool to execute
            input_data: Input data for the tool
            config: Optional configuration for the tool

        Returns:
            Tool execution result
        """
        tool_wrapper = self.create_tool_instance(tool_name, config)
        formatted_input = tool_wrapper.format_input(input_data)
        result = await tool_wrapper.tool.ainvoke(formatted_input)
        return tool_wrapper.format_output(result)

    def collect_tools_info(self) -> tuple[str, str]:
        """
        Collect information about available and activated tools.

        Returns:
            Tuple of (validated_tools_info, activated_tools_info)
        """
        return collect_tools(self.workflow_config)

    def get_tool_by_name(self, tool_name: str) -> Optional[Any]:
        """
        Get a validated tool by name.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool instance if found, None otherwise
        """
        for tool in self.workflow_config.validated_tools:
            if tool.name == tool_name:
                return tool
        return None

    def list_available_tools(self) -> List[str]:
        """
        Get list of all available tool names.

        Returns:
            List of tool names
        """
        return [tool.name for tool in self.workflow_config.validated_tools]

    def list_activated_tools(self) -> List[str]:
        """
        Get list of activated tool names.

        Returns:
            List of activated tool names
        """
        return [tool.name for tool in self.workflow_config.activated_tools]

    def get_workflow_config(self) -> WorkflowConfig:
        """
        Get the current workflow configuration.

        Returns:
            WorkflowConfig instance
        """
        return self.workflow_config

    def update_workflow_config(self, new_config: WorkflowConfig):
        """
        Update the workflow configuration.

        Args:
            new_config: New workflow configuration
        """
        self.workflow_config = new_config
