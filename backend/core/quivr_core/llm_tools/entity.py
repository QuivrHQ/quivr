from quivr_core.base_config import QuivrBaseConfig
from typing import Callable


class ToolsCategory(QuivrBaseConfig):
    name: str
    description: str
    tools: list
    default_tool: str | None = None
    create_tool: Callable

    def __init__(self, **data):
        super().__init__(**data)
        self.name = self.name.lower()
