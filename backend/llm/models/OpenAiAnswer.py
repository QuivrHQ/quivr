from typing import Optional

from .FunctionCall import FunctionCall


class OpenAiAnswer:
    def __init__(
        self,
        content: Optional[str] = None,
        function_call: FunctionCall = None,  # pyright: ignore reportPrivateUsage=none
    ):
        self.content = content
        self.function_call = function_call
