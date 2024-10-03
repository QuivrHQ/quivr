from quivr_core.base_config import QuivrBaseConfig


class ToolsCategory(QuivrBaseConfig):
    name: str
    description: str
    tools: list
    default_tool: str
