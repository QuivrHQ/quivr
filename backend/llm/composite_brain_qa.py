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
                "required": ["brain_id", "question"],
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

            print(response)

        print("connected_brains", connected_brains)
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

        print("tools", tools)
        print("available_functions", available_functions)
        print("connected_brains_details", connected_brains_details)
        CHOOSE_BRAIN_FROM_TOOLS_PROMPT = (
            "Based on the provided user content, find the most appropriate tools to answer"
            + "If you can't find any tool to answer and only then, and if you can answer without using any tool. In that case, let the user know that you are not using any particular brain (i.e tool) "
            # Pour diminuer le risque d'avoir des boucles
            + "what has been called before: nom de la fonction + argument, dont call unless really needed"
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

        print("\nFirst LLM Response:\n", response)

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

        called_tools_log = []

        if tool_calls:
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                queried_brain = connected_brains_details[function_name]
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print("function_args", function_args["question"])
                question = ChatQuestion(question=function_args["question"])
                function_response = function_to_call(
                    chat_id=chat_id,
                    question=question,
                    save_answer=False,
                )

                called_tools_log.append(
                    {
                        "log_message": f"🧠< Querying the brain {queried_brain.name} with the following arguments: {function_args} >🧠",
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response.assistant,
                    }
                )

            PROMPT_2 = "If initial question can be answered by our converaation messsages, then give an answer and end the conversation. \
                        Otherwise, ask a new question to the assistant and choose brains you would like to ask questions."

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

            print("\nSecond LLM response:\n", response_after_tools_answers)

            if response_after_tools_answers.choices[0].finish_reason == "stop":
                answer = response_after_tools_answers.choices[0].message.content
                print("ANSWER 2", answer)
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
    ) -> str:
        connected_brains = brain_service.get_connected_brains(self.brain_id)
        if not connected_brains:
            yield HeadlessQA(
                chat_id=chat_id,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                streaming=self.streaming,
                prompt_id=self.prompt_id,
            ).generate_stream(chat_id, question)

        print("connected_brains", connected_brains)
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

        print("tools", tools)
        print("available_functions", available_functions)
        print("connected_brains_details", connected_brains_details)
        CHOOSE_BRAIN_FROM_TOOLS_PROMPT = (
            "Based on the provided user content, find the most appropriate tools to answer"
            + "If you can't find any tool to answer and only then, and if you can answer without using any tool. In that case, let the user know that you are not using any particular brain (i.e tool) "
            # Pour diminuer le risque d'avoir des boucles
            + "what has been called before: nom de la fonction + argument, dont call unless really needed"
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

        initial_response = completion(
            model="gpt-3.5-turbo",
            messages=messages,  # is History included ?
            tools=tools,
            tool_choice="auto",
        )

        yield initial_response.choices[0].message

        print("\nFirst LLM Response:\n", initial_response)

        if initial_response.choices[0].finish_reason == "stop":
            answer = initial_response.choices[0].message
            print("ANSWER 1", answer)
            if save_answer:
                streamed_chat_history = chat_service.update_chat_history(
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

                streamed_chat_history = GetChatHistoryOutput(
                    **{
                        "chat_id": chat_id,
                        "user_message": question.question,
                        "assistant": answer,
                        "message_time": streamed_chat_history.message_time,
                        "prompt_title": self.prompt_to_use.title
                        if self.prompt_to_use
                        else None,
                        "brain_name": brain.name if brain else None,
                        "message_id": streamed_chat_history.message_id,
                    }
                )

            streamed_chat_history = GetChatHistoryOutput(
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

        response_message = initial_response.choices[0].message
        tool_calls = response_message.tool_calls

        called_tools_log = []

        if tool_calls:
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                queried_brain = connected_brains_details[function_name]
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print("function_args", function_args["question"])
                question = ChatQuestion(question=function_args["question"])
                function_response = function_to_call(
                    chat_id=chat_id,
                    question=question,
                    save_answer=False,
                )

                called_tools_log.append(
                    {
                        "log_message": f"🧠< Querying the brain {queried_brain.name} with the following arguments: {function_args} >🧠",
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response.assistant,
                    }
                )

            PROMPT_2 = "If initial question can be answered by our converaation messsages, then give an answer and end the conversation. \
                        Otherwise, ask a new question to the assistant and choose brains you would like to ask questions."

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

            print("\nSecond LLM response:\n", response_after_tools_answers)

            if response_after_tools_answers.choices[0].finish_reason == "stop":
                answer = response_after_tools_answers.choices[0].message.content
                print("ANSWER 2", answer)
                if save_answer:
                    streamed_chat_history = chat_service.update_chat_history(
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

                    streamed_chat_history = GetChatHistoryOutput(
                        **{
                            "chat_id": chat_id,
                            "user_message": question.question,
                            "assistant": answer,
                            "message_time": streamed_chat_history.message_time,
                            "prompt_title": self.prompt_to_use.title
                            if self.prompt_to_use
                            else None,
                            "brain_name": brain.name if brain else None,
                            "message_id": streamed_chat_history.message_id,
                        }
                    )

                    yield streamed_chat_history
                streamed_chat_history = GetChatHistoryOutput(
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
                yield streamed_chat_history

            print("response_after_tools_answers", response_after_tools_answers)

            streamed_chat_history = GetChatHistoryOutput(
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

            yield streamed_chat_history
