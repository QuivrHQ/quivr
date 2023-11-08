import json
from typing import Optional
from uuid import UUID

from langchain.schema import FunctionMessage
from litellm import completion
from models.chats import ChatQuestion
from models.databases.supabase.chats import CreateChatHistory
from repository.brain.get_brain_by_id import get_brain_by_id
from repository.chat.format_chat_history import (
    format_chat_history,
    format_history_to_openai_mesages,
)
from repository.chat.get_chat_history import get_chat_history
from repository.chat.update_chat_history import update_chat_history
from repository.chat.update_message_by_id import update_message_by_id

from llm.qa_base import QABaseBrainPicking
from llm.utils.call_brain_api import call_brain_api
from llm.utils.get_api_brain_definition_as_json_schema import (
    get_api_brain_definition_as_json_schema,
)


class APIBrainQA(QABaseBrainPicking):
    user_id: UUID

    def __init__(
        self,
        model: str,
        brain_id: str,
        chat_id: str,
        user_id: UUID,
        streaming: bool = False,
        prompt_id: Optional[UUID] = None,
        **kwargs,
    ):
        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
            prompt_id=prompt_id,
            **kwargs,
        )
        self.user_id = user_id

    async def generate_stream(self, chat_id: UUID, question: ChatQuestion):
        if not question.brain_id:
            raise Exception("No brain id provided")

        history = get_chat_history(self.chat_id)
        prompt_content = self.prompt_to_use.content if self.prompt_to_use else ""
        brain = get_brain_by_id(question.brain_id)
        if not brain:
            raise Exception("No brain found")

        messages = format_history_to_openai_mesages(
            format_chat_history(history),
            prompt_content,
            question.question,
        )

        response = completion(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=messages,
            functions=[get_api_brain_definition_as_json_schema(brain)],
            stream=True,
        )

        if response.choices[0].finish_reason == "function_call":
            arguments = json.load(
                response.choices[0].message["function_call"]["arguments"]
            )

            content = call_brain_api(
                brain_id=question.brain_id, user_id=self.user_id, arguments=arguments
            )
            messages.append(FunctionMessage(name=brain.name, content=content))

            response = completion(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=messages,
                stream=True,
            )

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
        streamed_chat_history = get_chat_history.GetChatHistoryOutput(
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

        for chunk in response:
            new_token = chunk["choices"][0]["delta"]
            streamed_chat_history.assistant = new_token
            response_tokens.append(new_token)
            yield f"data: {json.dumps(streamed_chat_history.dict())}"

        update_message_by_id(
            message_id=str(streamed_chat_history.message_id),
            user_message=question.question,
            assistant="".join(response_tokens),
        )
