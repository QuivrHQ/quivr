from typing import Any, Dict  # For type hinting

from llm.BrainPickingOpenAIFunctions.models.FunctionCall import FunctionCall
from llm.BrainPickingOpenAIFunctions.models.OpenAiAnswer import OpenAiAnswer


def format_answer(model_response: Dict[str, Any]) -> OpenAiAnswer:
    answer = model_response["choices"][0]["message"]
    content = answer["content"]
    function_call = None

    if answer.get("function_call", None) is not None:
        function_call = FunctionCall(
            answer["function_call"]["name"],
            answer["function_call"]["arguments"],
        )

    return OpenAiAnswer(content=content, function_call=function_call)
