import json
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from litellm import completion
from llm.api_brain_qa import APIBrainQA
from llm.knowledge_brain_qa import KnowledgeBrainQA
from llm.qa_headless import HeadlessQA
from logger import get_logger
from modules.brain.entity.brain_entity import BrainEntity, BrainType
from modules.brain.service.brain_service import BrainService
from modules.chat.dto.chats import ChatQuestion
from modules.chat.dto.inputs import CreateChatHistory
from modules.chat.dto.outputs import GetChatHistoryOutput
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
                    "brain": {
                        "type": "string",
                        "description": "Brain details, need to check type too",
                    },
                    "question": {
                        "type": "string",
                        "description": "Question to ask the brain",
                    },
                },
                "required": ["brain", "question"],
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
                brain_id=brain.id,
                chat_id=self.chat_id,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                streaming=self.streaming,
                prompt_id=self.prompt_id,
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

    def get_stream_answer_generator_from_brain_type(self, brain: BrainEntity):
        if brain.brain_type == BrainType.COMPOSITE:
            return self.generate_stream
        elif brain.brain_type == BrainType.API:
            return APIBrainQA(
                brain_id=brain.id,
                chat_id=self.chat_id,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                streaming=self.streaming,
                prompt_id=self.prompt_id,
            ).generate_stream
        elif brain.brain_type == BrainType.DOC:
            return KnowledgeBrainQA(
                brain_id=str(brain.id),
                chat_id=self.chat_id,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                streaming=self.streaming,
                prompt_id=self.prompt_id,
            ).generate_stream

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool
    ) -> str:
        connected_brains = brain_service.get_connected_brains(self.brain_id)
        if not connected_brains:
            response = HeadlessQA(
                chat_id=chat_id,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                streaming=self.streaming,
                prompt_id=self.prompt_id,
            ).generate_answer(chat_id, question)
            brain = brain_service.get_brain_by_id(self.brain_id)
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
                        "prompt_title": self.prompt_to_use.title
                        if self.prompt_to_use
                        else None,
                        "brain_name": brain.name,
                        "message_id": new_chat.message_id,
                    }
                )
            return GetChatHistoryOutput(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": response.assistant,
                    "message_time": None,
                    "prompt_title": self.prompt_to_use.title
                    if self.prompt_to_use
                    else None,
                    "brain_name": brain.name,
                    "message_id": None,
                }
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
            messages.extend(formatted_message)

        messages.append({"role": "user", "content": question.question})

        response = completion(
            model="gpt-3.5-turbo",
            messages=messages,  # is History included ?
            tools=tools,
            tool_choice="auto",
        )

        if response.choices[0].finish_reason == "stop":
            answer = response.choices[0].message
            print("ANSWER 1", answer)
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
                        "assistant": answer,
                        "message_time": new_chat.message_time,
                        "prompt_title": self.prompt_to_use.title
                        if self.prompt_to_use
                        else None,
                        "brain_name": brain.name if brain else None,
                        "message_id": new_chat.message_id,
                    }
                )

            return GetChatHistoryOutput(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": answer,
                    "message_time": None,
                    "prompt_title": self.prompt_to_use.title
                    if self.prompt_to_use
                    else None,
                    "brain_name": None,
                    "message_id": None,
                }
            )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                question = ChatQuestion(question=function_args["question"])

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

            PROMPT_2 = "If initial question can be answered by our converaation messsages, then give an answer and end the conversation."

            messages.append({"role": "system", "content": PROMPT_2})

            for idx, msg in enumerate(messages):
                logger.info(
                    f"Message {idx}: Role - {msg['role']}, Content - {msg['content']}"
                )

            response_after_tools_answers = completion(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            if response_after_tools_answers.choices[0].finish_reason == "stop":
                answer = response_after_tools_answers.choices[0].message.content
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
                            "assistant": answer,
                            "message_time": new_chat.message_time,
                            "prompt_title": self.prompt_to_use.title
                            if self.prompt_to_use
                            else None,
                            "brain_name": brain.name if brain else None,
                            "message_id": new_chat.message_id,
                        }
                    )
                return GetChatHistoryOutput(
                    **{
                        "chat_id": chat_id,
                        "user_message": question.question,
                        "assistant": answer,
                        "message_time": "123",
                        "prompt_title": None,
                        "brain_name": brain.name,
                        "message_id": None,
                    }
                )

            print("response_after_tools_answers", response_after_tools_answers)

            return GetChatHistoryOutput(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": response_after_tools_answers.choices[0].message,
                    "message_time": "123",
                    "prompt_title": None,
                    "brain_name": brain.name,
                    "message_id": None,
                }
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
                    "prompt_title": self.prompt_to_use.title
                    if self.prompt_to_use
                    else None,
                    "brain_name": brain.name if brain else None,
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
                    "prompt_title": self.prompt_to_use.title
                    if self.prompt_to_use
                    else None,
                    "brain_name": brain.name if brain else None,
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
            model="gpt-3.5-turbo",
            stream=True,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        response_tokens = []
        tool_calls_aggregate = []
        for chunk in initial_response:
            # print("chunk", chunk)
            # print("chunk.choices [0].delta.content", chunk.choices[0].delta.content)
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
                    question = ChatQuestion(question=function_args["question"])

                    # yield f"🧠< Querying the brain {queried_brain.name} with the following arguments: {function_args} >🧠",

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

                PROMPT_2 = "If initial question can be answered by our conversation messages, then give an answer and end the conversation."
                # Otherwise, ask a new question to the assistant and choose brains you would like to ask questions."

                messages.append({"role": "system", "content": PROMPT_2})

                response_after_tools_answers = completion(
                    model="gpt-3.5-turbo",
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
