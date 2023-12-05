import json
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from litellm import completion
from models.chats import ChatQuestion
from models.databases.supabase.chats import CreateChatHistory
from repository.brain.get_brain_by_id import get_brain_by_id
from repository.chat.get_chat_history import GetChatHistoryOutput, get_chat_history
from repository.chat.update_chat_history import update_chat_history
from repository.chat.update_message_by_id import update_message_by_id

from llm.qa_base import QABaseBrainPicking
from llm.utils.call_brain_api import call_brain_api
from llm.utils.get_api_brain_definition_as_json_schema import (
    get_api_brain_definition_as_json_schema,
)


class APIBrainQA(
    QABaseBrainPicking,
):
    user_id: UUID

    def __init__(
        self,
        model: str,
        brain_id: str,
        chat_id: str,
        streaming: bool = False,
        prompt_id: Optional[UUID] = None,
        **kwargs,
    ):
        user_id = kwargs.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Cannot find user id")

        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
            prompt_id=prompt_id,
            **kwargs,
        )
        self.user_id = user_id

    async def make_completion(
        self,
        messages,
        functions,
        brain_id: UUID,
    ):
        response = completion(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=messages,
            functions=functions,
            stream=True,
            function_call="auto",
        )

        function_call = {
            "name": None,
            "arguments": "",
        }
        for chunk in response:
            finish_reason = chunk.choices[0].finish_reason

            if finish_reason == "stop":
                break

            if "function_call" in chunk.choices[0].delta:
                if "name" in chunk.choices[0].delta["function_call"]:
                    function_call["name"] = chunk.choices[0].delta["function_call"][
                        "name"
                    ]
                if "arguments" in chunk.choices[0].delta["function_call"]:
                    function_call["arguments"] += chunk.choices[0].delta[
                        "function_call"
                    ]["arguments"]

            elif finish_reason == "function_call":
                try:
                    arguments = json.loads(function_call["arguments"])
                except Exception:
                    arguments = {}

                api_call_response = call_brain_api(
                    brain_id=brain_id,
                    user_id=self.user_id,
                    arguments=arguments,
                )

                messages.append(
                    {
                        "role": "function",
                        "name": function_call["name"],
                        "content": api_call_response,
                    }
                )
                async for value in self.make_completion(
                    messages=messages,
                    functions=functions,
                    brain_id=brain_id,
                ):
                    yield value

            else:
                content = chunk.choices[0].delta.content
                yield content

    async def generate_stream(self, chat_id: UUID, question: ChatQuestion):
        if not question.brain_id:
            raise HTTPException(
                status_code=400, detail="No brain id provided in the question"
            )

        brain = get_brain_by_id(question.brain_id)

        if not brain:
            raise HTTPException(status_code=404, detail="Brain not found")

        prompt_content = "You'are a helpful assistant which can call APIs. Feel free to call the API when you need to. Don't force APIs call, do it when necessary. If it seems like you should call the API and there are missing parameters, ask user for them."

        if self.prompt_to_use:
            prompt_content += self.prompt_to_use.content

        messages = [{"role": "system", "content": prompt_content}]

        history = get_chat_history(self.chat_id)

        for message in history:
            formatted_message = [
                {"role": "user", "content": message.user_message},
                {"role": "assistant", "content": message.assistant},
            ]
            messages.extend(formatted_message)

        messages.append({"role": "user", "content": question.question})

        streamed_chat_history = update_chat_history(
            CreateChatHistory(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": "",
                    "brain_id": question.brain_id,
                    "prompt_id": self.prompt_to_use_id,
                }
            )
        )
        streamed_chat_history = GetChatHistoryOutput(
            **{
                "chat_id": str(chat_id),
                "message_id": streamed_chat_history.message_id,
                "message_time": streamed_chat_history.message_time,
                "user_message": question.question,
                "assistant": "",
                "prompt_title": self.prompt_to_use.title
                if self.prompt_to_use
                else None,
                "brain_name": brain.name if brain else None,
            }
        )
        response_tokens = []
        async for value in self.make_completion(
            messages=messages,
            functions=[get_api_brain_definition_as_json_schema(brain)],
            brain_id=question.brain_id,
        ):
            streamed_chat_history.assistant = value
            response_tokens.append(value)
            yield f"data: {json.dumps(streamed_chat_history.dict())}"

        update_message_by_id(
            message_id=str(streamed_chat_history.message_id),
            user_message=question.question,
            assistant="".join(response_tokens),
        )
