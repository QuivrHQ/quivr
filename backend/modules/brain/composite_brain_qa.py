import json
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from litellm import completion
from logger import get_logger
from modules.brain.api_brain_qa import APIBrainQA
from modules.brain.entity.brain_entity import BrainEntity, BrainType
from modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from modules.brain.qa_headless import HeadlessQA
from modules.brain.service.brain_service import BrainService
from modules.chat.dto.chats import ChatQuestion
from modules.chat.dto.inputs import CreateChatHistory
from modules.chat.dto.outputs import (
    BrainCompletionOutput,
    CompletionMessage,
    CompletionResponse,
    GetChatHistoryOutput,
)
from modules.chat.service.chat_service import ChatService

brain_service = BrainService()
chat_service = ChatService()

logger = get_logger(__name__)


def format_brain_to_tool(brain):
    return {
        "type": "function",
        "function": {
            "name": str(brain.id),
            "description": brain.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Question to ask the brain",
                    },
                },
                "required": ["question"],
            },
        },
    }


class CompositeBrainQA(
    KnowledgeBrainQA,
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

    def get_answer_generator_from_brain_type(self, brain: BrainEntity):
        if brain.brain_type == BrainType.COMPOSITE:
            return self.generate_answer
        elif brain.brain_type == BrainType.API:
            return APIBrainQA(
                brain_id=str(brain.id),
                chat_id=self.chat_id,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                streaming=self.streaming,
                prompt_id=self.prompt_id,
                user_id=str(self.user_id),
                raw=brain.raw,
                jq_instructions=brain.jq_instructions,
            ).generate_answer
        elif brain.brain_type == BrainType.DOC:
            return KnowledgeBrainQA(
                brain_id=str(brain.id),
                chat_id=self.chat_id,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                streaming=self.streaming,
                prompt_id=self.prompt_id,
            ).generate_answer

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool
    ) -> str:
        brain = brain_service.get_brain_by_id(question.brain_id)

        connected_brains = brain_service.get_connected_brains(self.brain_id)

        if not connected_brains:
            response = HeadlessQA(
                chat_id=chat_id,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                streaming=self.streaming,
                prompt_id=self.prompt_id,
            ).generate_answer(chat_id, question, save_answer=False)
            if save_answer:
                new_chat = chat_service.update_chat_history(
                    CreateChatHistory(
                        **{
                            "chat_id": chat_id,
                            "user_message": question.question,
                            "assistant": response.assistant,
                            "brain_id": question.brain_id,
                            "prompt_id": self.prompt_to_use_id,
                        }
                    )
                )
                return GetChatHistoryOutput(
                    **{
                        "chat_id": chat_id,
                        "user_message": question.question,
                        "assistant": response.assistant,
                        "message_time": new_chat.message_time,
                        "prompt_title": (
                            self.prompt_to_use.title if self.prompt_to_use else None
                        ),
                        "brain_name": brain.name,
                        "message_id": new_chat.message_id,
                        "brain_id": str(brain.id),
                    }
                )
            return GetChatHistoryOutput(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": response.assistant,
                    "message_time": None,
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": brain.name,
                    "message_id": None,
                    "brain_id": str(brain.id),
                }
            )

        tools = []
        available_functions = {}

        connected_brains_details = {}
        for connected_brain_id in connected_brains:
            connected_brain = brain_service.get_brain_by_id(connected_brain_id)
            if connected_brain is None:
                continue

            tools.append(format_brain_to_tool(connected_brain))

            available_functions[connected_brain_id] = (
                self.get_answer_generator_from_brain_type(connected_brain)
            )

            connected_brains_details[str(connected_brain.id)] = connected_brain

        CHOOSE_BRAIN_FROM_TOOLS_PROMPT = (
            "Based on the provided user content, find the most appropriate tools to answer"
            + "If you can't find any tool to answer and only then, and if you can answer without using any tool. In that case, let the user know that you are not using any particular brain (i.e tool) "
        )

        messages = [{"role": "system", "content": CHOOSE_BRAIN_FROM_TOOLS_PROMPT}]

        history = chat_service.get_chat_history(self.chat_id)

        for message in history:
            formatted_message = [
                {"role": "user", "content": message.user_message},
                {"role": "assistant", "content": message.assistant},
            ]
            messages.extend(formatted_message)

        messages.append({"role": "user", "content": question.question})

        response = completion(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        brain_completion_output = self.make_recursive_tool_calls(
            messages,
            question,
            chat_id,
            tools,
            available_functions,
            recursive_count=0,
            last_completion_response=response.choices[0],
        )

        if brain_completion_output:
            answer = brain_completion_output.response.message.content
            new_chat = None
            if save_answer:
                new_chat = chat_service.update_chat_history(
                    CreateChatHistory(
                        **{
                            "chat_id": chat_id,
                            "user_message": question.question,
                            "assistant": answer,
                            "brain_id": question.brain_id,
                            "prompt_id": self.prompt_to_use_id,
                        }
                    )
                )
            return GetChatHistoryOutput(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": brain_completion_output.response.message.content,
                    "message_time": new_chat.message_time if new_chat else None,
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": brain.name if brain else None,
                    "message_id": new_chat.message_id if new_chat else None,
                    "brain_id": str(brain.id) if brain else None,
                }
            )

    def make_recursive_tool_calls(
        self,
        messages,
        question,
        chat_id,
        tools=[],
        available_functions={},
        recursive_count=0,
        last_completion_response: CompletionResponse = None,
    ):
        if recursive_count > 5:
            print(
                "The assistant is having issues and took more than 5 calls to the tools. Please try again later or an other instruction."
            )
            return None

        finish_reason = last_completion_response.finish_reason
        if finish_reason == "stop":
            messages.append(last_completion_response.message)
            return BrainCompletionOutput(
                **{
                    "messages": messages,
                    "question": question.question,
                    "response": last_completion_response,
                }
            )

        if finish_reason == "tool_calls":
            response_message: CompletionMessage = last_completion_response.message
            tool_calls = response_message.tool_calls

            messages.append(response_message)

            if (
                len(tool_calls) == 0
                or tool_calls is None
                or len(available_functions) == 0
            ):
                return

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                question = ChatQuestion(
                    question=function_args["question"], brain_id=function_name
                )

                # TODO: extract chat_id from generate_answer function of XBrainQA
                function_response = function_to_call(
                    chat_id=chat_id,
                    question=question,
                    save_answer=False,
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response.assistant,
                    }
                )

            PROMPT_2 = "If initial question can be answered by our conversation messages, then give an answer and end the conversation."

            messages.append({"role": "system", "content": PROMPT_2})

            for idx, msg in enumerate(messages):
                logger.info(
                    f"Message {idx}: Role - {msg['role']}, Content - {msg['content']}"
                )

            response_after_tools_answers = completion(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            return self.make_recursive_tool_calls(
                messages,
                question,
                chat_id,
                tools,
                available_functions,
                recursive_count=recursive_count + 1,
                last_completion_response=response_after_tools_answers.choices[0],
            )

    async def generate_stream(
        self,
        chat_id: UUID,
        question: ChatQuestion,
        save_answer: bool,
        should_log_steps: Optional[bool] = True,
    ):
        brain = brain_service.get_brain_by_id(question.brain_id)
        if save_answer:
            streamed_chat_history = chat_service.update_chat_history(
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
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": brain.name if brain else None,
                    "brain_id": str(brain.id) if brain else None,
                }
            )
        else:
            streamed_chat_history = GetChatHistoryOutput(
                **{
                    "chat_id": str(chat_id),
                    "message_id": None,
                    "message_time": None,
                    "user_message": question.question,
                    "assistant": "",
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": brain.name if brain else None,
                    "brain_id": str(brain.id) if brain else None,
                }
            )

        connected_brains = brain_service.get_connected_brains(self.brain_id)

        if not connected_brains:
            headlesss_answer = HeadlessQA(
                chat_id=chat_id,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                streaming=self.streaming,
                prompt_id=self.prompt_id,
            ).generate_stream(chat_id, question)

            response_tokens = []
            async for value in headlesss_answer:
                streamed_chat_history.assistant = value
                response_tokens.append(value)
                yield f"data: {json.dumps(streamed_chat_history.dict())}"

            if save_answer:
                chat_service.update_message_by_id(
                    message_id=str(streamed_chat_history.message_id),
                    user_message=question.question,
                    assistant="".join(response_tokens),
                )

        tools = []
        available_functions = {}

        connected_brains_details = {}
        for brain_id in connected_brains:
            brain = brain_service.get_brain_by_id(brain_id)
            if brain == None:
                continue

            tools.append(format_brain_to_tool(brain))

            available_functions[brain_id] = self.get_answer_generator_from_brain_type(
                brain
            )

            connected_brains_details[str(brain.id)] = brain

        CHOOSE_BRAIN_FROM_TOOLS_PROMPT = (
            "Based on the provided user content, find the most appropriate tools to answer"
            + "If you can't find any tool to answer and only then, and if you can answer without using any tool. In that case, let the user know that you are not using any particular brain (i.e tool) "
        )

        messages = [{"role": "system", "content": CHOOSE_BRAIN_FROM_TOOLS_PROMPT}]

        history = chat_service.get_chat_history(self.chat_id)

        for message in history:
            formatted_message = [
                {"role": "user", "content": message.user_message},
                {"role": "assistant", "content": message.assistant},
            ]
            if message.assistant is None:
                print(message)
            messages.extend(formatted_message)

        messages.append({"role": "user", "content": question.question})

        initial_response = completion(
            model="gpt-3.5-turbo-0125",
            stream=True,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        response_tokens = []
        tool_calls_aggregate = []
        for chunk in initial_response:
            content = chunk.choices[0].delta.content
            if content is not None:
                # Need to store it ?
                streamed_chat_history.assistant = content
                response_tokens.append(chunk.choices[0].delta.content)

                if save_answer:
                    yield f"data: {json.dumps(streamed_chat_history.dict())}"
                else:
                    yield f"🧠<' {chunk.choices[0].delta.content}"

            if (
                "tool_calls" in chunk.choices[0].delta
                and chunk.choices[0].delta.tool_calls is not None
            ):
                tool_calls = chunk.choices[0].delta.tool_calls
                for tool_call in tool_calls:
                    id = tool_call.id
                    name = tool_call.function.name
                    if id and name:
                        tool_calls_aggregate += [
                            {
                                "id": tool_call.id,
                                "function": {
                                    "arguments": tool_call.function.arguments,
                                    "name": tool_call.function.name,
                                },
                                "type": "function",
                            }
                        ]

                    else:
                        try:
                            tool_calls_aggregate[tool_call.index]["function"][
                                "arguments"
                            ] += tool_call.function.arguments
                        except IndexError:
                            print("TOOL_CALL_INDEX error", tool_call.index)
                            print("TOOL_CALLS_AGGREGATE error", tool_calls_aggregate)

            finish_reason = chunk.choices[0].finish_reason

            if finish_reason == "stop":
                if save_answer:
                    chat_service.update_message_by_id(
                        message_id=str(streamed_chat_history.message_id),
                        user_message=question.question,
                        assistant="".join(
                            [
                                token
                                for token in response_tokens
                                if not token.startswith("🧠<")
                            ]
                        ),
                    )
                break

            if finish_reason == "tool_calls":
                messages.append(
                    {
                        "role": "assistant",
                        "tool_calls": tool_calls_aggregate,
                        "content": None,
                    }
                )
                for tool_call in tool_calls_aggregate:
                    function_name = tool_call["function"]["name"]
                    queried_brain = connected_brains_details[function_name]
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call["function"]["arguments"])
                    print("function_args", function_args["question"])
                    question = ChatQuestion(
                        question=function_args["question"], brain_id=queried_brain.id
                    )

                    # yield f"🧠< Querying the brain {queried_brain.name} with the following arguments: {function_args} >🧠",

                    print(
                        f"🧠< Querying the brain {queried_brain.name} with the following arguments: {function_args}",
                    )
                    function_response = function_to_call(
                        chat_id=chat_id,
                        question=question,
                        save_answer=False,
                    )

                    messages.append(
                        {
                            "tool_call_id": tool_call["id"],
                            "role": "tool",
                            "name": function_name,
                            "content": function_response.assistant,
                        }
                    )

                    print("messages", messages)

                PROMPT_2 = "If the last user's question can be answered by our conversation messages since then, then give an answer and end the conversation. If you need to ask question to the user to gather more information and give a more accurate answer, then ask the question and wait for the user's answer."
                # Otherwise, ask a new question to the assistant and choose brains you would like to ask questions."

                messages.append({"role": "system", "content": PROMPT_2})

                response_after_tools_answers = completion(
                    model="gpt-3.5-turbo-0125",
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    stream=True,
                )

                response_tokens = []
                for chunk in response_after_tools_answers:
                    print("chunk_response_after_tools_answers", chunk)
                    content = chunk.choices[0].delta.content
                    if content:
                        streamed_chat_history.assistant = content
                        response_tokens.append(chunk.choices[0].delta.content)
                        yield f"data: {json.dumps(streamed_chat_history.dict())}"

                    finish_reason = chunk.choices[0].finish_reason

                    if finish_reason == "stop":
                        chat_service.update_message_by_id(
                            message_id=str(streamed_chat_history.message_id),
                            user_message=question.question,
                            assistant="".join(
                                [
                                    token
                                    for token in response_tokens
                                    if not token.startswith("🧠<")
                                ]
                            ),
                        )
                        break
                    elif finish_reason is not None:
                        # TODO: recursively call with tools (update prompt + create intermediary function )
                        print("NO STOP")
                        print(chunk.choices[0])
