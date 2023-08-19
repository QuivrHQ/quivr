from typing import Optional
from typing import Any, Dict


class FunctionCall:
    def __init__(
        self,
        name: Optional[str] = None,
        arguments: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.arguments = arguments
