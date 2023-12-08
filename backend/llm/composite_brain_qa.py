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
                # "exclude": ["brain_id" dans visited_brains + question like questions dans asked_questions[brain_id]]
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
        print("BRAIN", brain)
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
        # brain_type_to_answer_generator = {
        #     "composite_brain": self.generate_answer,
        #     "api_brain": APIBrainQA(
        #         brain_id=brain.id,
        #         chat_id=self.chat_id,
        #         model=self.model,
        #         max_tokens=self.max_tokens,
        #         temperature=self.temperature,
        #         streaming=self.streaming,
        #         prompt_id=self.prompt_id,
        #     ).generate_answer,
        #     "knowledge_brain": KnowledgeBrainQA(
        #         brain_id=brain.id,
        #         chat_id=self.chat_id,
        #         model=self.model,
        #         max_tokens=self.max_tokens,
        #         temperature=self.temperature,
        #         streaming=self.streaming,
        #         prompt_id=self.prompt_id,
        #     ).generate_answer,
        # }
        # return brain_type_to_answer_generator.get(brain.brain_type)

    def generate_answer(self, chat_id: UUID, question: ChatQuestion) -> str:
        # Retrieve the connected brains for the current composite brain
        connected_brains = brain_service.get_connected_brains(self.brain_id)
        if not connected_brains:
            # If no connected brains, default to regular HeadlessQA
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

        # Create tools from the connected brains similarly to this:
        for brain_id in connected_brains:
            brain = brain_service.get_brain_by_id(brain_id)
            if brain == None:
                continue

            tools.append(format_brain_to_tool(brain))

            print("tools", tools)

            available_functions[brain_id] = self.get_answer_generator_from_brain_type(
                brain
            )
            print("available_functions", available_functions)

        print("tools", tools)
        print("available_functions", available_functions)

        CHOOSE_BRAIN_FROM_TOOLS_PROMPT = (
            "Based on the provided user content, find the most appropriate tools to answer"
            + "If you can't find any tool to answer and only then, and if you can answer without using any tool, please do so with a 3 year old assistant personality. In that case, let the user know that you are not using any particular brain (i.e tool) "
            # Pour diminuer le risque d'avoir des boucles
            + "what has been called before: nom de la fonction + argument, dont call unless really needed"
        )

        # Have all the steps and answers logged in a document that will be passed to emettre l'intention et creer les tool_calls
        # Call completion with this tools
        # Assuming question.question is a string
        messages = [
            {"role": "user", "content": question.question},
            # add quivr or brain prompt: Helpful assistant bla bla bla
            {"role": "system", "content": CHOOSE_BRAIN_FROM_TOOLS_PROMPT},
        ]
        # Add any additional messages to this list as needed

        response = completion(
            model="gpt-3.5-turbo",
            messages=messages,  # Pass the correctly formatted messages
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )

        print("\nFirst LLM Response:\n", response)

        # backend-core  | First LLM Response:
        # backend-core  |  ModelResponse(id='chatcmpl-8TTmScnbGzs5gX0SePNxzbg0y8K0E', choices=[Choices(finish_reason='tool_calls', index=0, message=Message(content=None, role='assistant', tool_calls=[ChatCompletionMessageToolCall(id='call_E6SXHf50pqbeg9cdE3WW1cte', function=Function(arguments='{"question":"What do you know about coffee?"}', name='3d71786c-f176-42b1-b7f5-9f40daaaf922'), type='function')]))], created=1702036680, model='gpt-3.5-turbo-1106', object='chat.completion', system_fingerprint='fp_eeff13170a', usage=Usage(completion_tokens=42, prompt_tokens=262, total_tokens=304), _response_ms=1505.449)

        # check if the finish_reason is stop
        if response.choices[0].finish_reason == "stop":
            return response.choices[0].message

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        print("\nLength of tool calls", len(tool_calls))

        called_tools_log = []
        # messages = [question.question]
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            messages.append(response_message)
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                print("tool to call", tool_call)

                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                print("function_args", function_args["question"])
                question = ChatQuestion(question=function_args["question"])
                function_response = function_to_call(
                    chat_id=chat_id,
                    question=question,
                )

                # store tool logs in a list as an object
                called_tools_log.append(
                    {
                        # get the actual brain name
                        "log_message": "🧠< Querying the brain {tool_call.function.name} with the following arguments: {tool_call.function.arguments} >🧠",
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
                )  # extend conversation with function response

            PROMPT_2 = "If initial question can be answered by our converaation messsages, then give an answer and end the conversation. \
                        Otherwise, ask a new question to the assistant and choose brains you would like to ask questions."

            messages.append({"role": "system", "content": PROMPT_2})

            for idx, msg in enumerate(messages):
                logger.info(
                    f"Message {idx}: Role - {msg['role']}, Content - {msg['content']}"
                )

            second_response = completion(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=tools,
                tool_choice="auto",  # auto is default, but we'll be explicit
            )  # get a new response from the model where it can see the function response

            print("\nSecond LLM response:\n", second_response)

            # update the chat history with the new response
            return GetChatHistoryOutput(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": second_response.choices[0].message.content,
                    "message_time": "123",
                    "prompt_title": None,
                    "brain_name": brain.name,
                    "message_id": "e3894199-6fa3-43e6-9fb4-7e3864f517eb",
                }
            )

        # add an intermediary function to handle recursive call:
        # condition d'arret: plus aucun tool calls
        # si pas de tool calls: return response
        # sinon: call intermediary_function_call avec les tool calls et le prompt updaté (PROMPT_2) + les derniers messages
        # check if any tools are to be called again
        # do the thing
        # else: answer

        # print("\nSecond LLM response:\n", second_response)
        # check second_response for function calls and repeat steps 2-4 if necessary
        # return response.choices[0].message
        # return GetChatHistoryOutput(
        #     **{
        #         "chat_id": chat_id,
        #         "user_message": question.question,
        #         "assistant": response.choices[0].message,
        #         "message_time": "123",
        #         "prompt_title": None,
        #         "brain_name": None,
        #         "message_id": 1234,
        #     }
        # )
