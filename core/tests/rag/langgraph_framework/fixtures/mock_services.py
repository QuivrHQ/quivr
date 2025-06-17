"""Mock services for testing."""

from typing import Optional, Any, Type

from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig


class MockLLMService:
    """Mock LLM service for testing."""

    def __init__(self, llm_config: Optional[LLMEndpointConfig] = None):
        self.llm_config = llm_config or LLMEndpointConfig()
        self.call_count = 0
        self.last_input: Optional[str] = None

    def generate(self, prompt: str) -> str:
        """Mock generation."""
        self.call_count += 1
        self.last_input = prompt
        return f"Generated response for: {prompt}"

    def supports_func_calling(self) -> bool:
        """Mock function calling support."""
        return True


class MockToolService:
    """Mock tool service for testing."""

    def __init__(self, workflow_config: Optional[WorkflowConfig] = None):
        self.workflow_config = workflow_config or WorkflowConfig()
        self.activated_tools: list[str] = []
        self.deactivated_tools: list[str] = []

    def activate_tool(self, tool_name: str):
        """Mock tool activation."""
        self.activated_tools.append(tool_name)

    def deactivate_tool(self, tool_name: str):
        """Mock tool deactivation."""
        self.deactivated_tools.append(tool_name)

    def get_node_tools(self, node_name: str):
        """Mock get node tools."""
        return [f"tool_for_{node_name}"]


class MockRAGPromptService:
    """Mock RAG prompt service for testing."""

    def __init__(self):
        self.template_calls = []

    def get_template(self, template_name: str) -> str:
        """Mock template retrieval."""
        self.template_calls.append(template_name)
        return f"Template for {template_name}"

    def format_prompt(self, template: str, **kwargs) -> str:
        """Mock prompt formatting."""
        return f"Formatted: {template} with {kwargs}"


class MockServiceFactory:
    """Mock service factory for testing."""

    def __init__(self, service_instance: Any, config_type: Optional[Type] = None):
        self.service_instance = service_instance
        self.config_type = config_type
        self.create_calls: list[Any] = []

    def create(self, config: Optional[Any] = None) -> Any:
        """Mock service creation."""
        self.create_calls.append(config)
        return self.service_instance

    def get_config_type(self) -> Optional[Type]:
        """Mock config type."""
        return self.config_type
