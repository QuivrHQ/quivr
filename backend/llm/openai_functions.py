from typing import Any, Dict, List, Optional

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from llm.models.FunctionCall import FunctionCall
from llm.models.OpenAiAnswer import OpenAiAnswer
from logger import get_logger
from models.chat import ChatHistory
from repository.chat.get_chat_history import get_chat_history
from repository.chat.update_chat_history import update_chat_history
from supabase import Client, create_client
from vectorstore.supabase import CustomSupabaseVectorStore

from .base import BaseBrainPicking

logger = get_logger(__name__)


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


class OpenAIFunctionsBrainPicking(BaseBrainPicking):
    """
    Class for the OpenAI Brain Picking functionality using OpenAI Functions.
    It allows to initialize a Chat model, generate questions and retrieve answers using ConversationalRetrievalChain.
    """

    # Default class attributes
    model: str = "gpt-3.5-turbo-0613"

    def __init__(
        self,
        model: str,
        chat_id: str,
        temperature: float,
        max_tokens: int,
        brain_id: str,
        user_openai_api_key: str,
        # TODO: add streaming
    ) -> "OpenAIFunctionsBrainPicking":
        super().__init__(
            model=model,
            chat_id=chat_id,
            max_tokens=max_tokens,
            user_openai_api_key=user_openai_api_key,
            temperature=temperature,
            brain_id=str(brain_id),
            streaming=False,
        )

    @property
    def openai_client(self) -> ChatOpenAI:
        return ChatOpenAI(openai_api_key=self.openai_api_key)

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(openai_api_key=self.openai_api_key)

    @property
    def supabase_client(self) -> Client:
        return create_client(
            self.brain_settings.supabase_url, self.brain_settings.supabase_service_key
        )

    @property
    def vector_store(self) -> CustomSupabaseVectorStore:
        return CustomSupabaseVectorStore(
            self.supabase_client,
            self.embeddings,
            table_name="vectors",
            brain_id=self.brain_id,
        )

    def _get_model_response(
        self,
        messages: List[Dict[str, str]],
        functions: Optional[List[Dict[str, Any]]] = None,
    ) -> Any:
        """
        Retrieve a model response given messages and functions
        """
        logger.info("Getting model response")
        kwargs = {
            "messages": messages,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if functions:
            logger.info("Adding functions to model response")
            kwargs["functions"] = functions

        return self.openai_client.completion_with_retry(**kwargs)

    def _get_chat_history(self) -> List[Dict[str, str]]:
        """
        Retrieves the chat history in a formatted list
        """
        logger.info("Getting chat history")
        history = get_chat_history(self.chat_id)
        return [
            item
            for chat in history
            for item in [
                {"role": "user", "content": chat.user_message},
                {"role": "assistant", "content": chat.assistant},
            ]
        ]

    def _get_context(self, question: str) -> str:
        """
        Retrieve documents related to the question
        """
        logger.info("Getting context")

        return self.vector_store.similarity_search(query=question)

    def _construct_prompt(
        self, question: str, useContext: bool = False, useHistory: bool = False
    ) -> List[Dict[str, str]]:
        """
        Constructs a prompt given a question, and optionally include context and history
        """
        logger.info("Constructing prompt")
        system_messages = [
            {
                "role": "system",
                "content": "Your name is Quivr. You are a second brain. A person will ask you a question and you will provide a helpful answer. Write the answer in the same language as the question. If you don't know the answer, just say that you don't know. Don't try to make up an answer. Our goal is to answer questions about user uploaded documents. Unless basic questions or greetings, you should always refer to user uploaded documents by fetching them with the get_history_and_context function. If the user ask a question that is not common knowledge for a 10 years old, then use get_history_and_context to find a document that can help you answer the question. If the user ask a question that is common knowledge for a 10 years old, then you can answer the question without using get_history_and_context.",
            }
        ]

        if useHistory:
            logger.info("Adding chat history to prompt")
            history = self._get_chat_history()
            system_messages.append(
                {"role": "system", "content": "Previous messages are already in chat."}
            )
            system_messages.extend(history)

        if useContext:
            logger.info("Adding chat context to prompt")
            chat_context = self._get_context(question)
            context_message = f"Here is chat context: {chat_context if chat_context else 'No document found'}"
            system_messages.append({"role": "user", "content": context_message})

        system_messages.append({"role": "user", "content": question})

        return system_messages

    def generate_answer(self, question: str) -> ChatHistory:
        """
        Main function to get an answer for the given question
        """
        logger.info("Getting answer")
        functions = [
            {
                "name": "get_history",
                "description": "Used to get the chat history between the user and the assistant",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "get_history_and_context",
                "description": "Used for retrieving documents related to the question to help answer the question and the previous chat history",
                "parameters": {"type": "object", "properties": {}},
            },
        ]

        # First, try to get an answer using just the question
        response = self._get_model_response(
            messages=self._construct_prompt(question), functions=functions
        )
        formatted_response = format_answer(response)

        # If the model calls for history, try again with history included
        if (
            formatted_response.function_call
            and formatted_response.function_call.name == "get_history"
        ):
            logger.info("Model called for history")
            response = self._get_model_response(
                messages=self._construct_prompt(question, useHistory=True),
                functions=[],
            )

            formatted_response = format_answer(response)

        if (
            formatted_response.function_call
            and formatted_response.function_call.name == "get_history_and_context"
        ):
            logger.info("Model called for history and context")
            response = self._get_model_response(
                messages=self._construct_prompt(
                    question, useContext=True, useHistory=True
                ),
                functions=[],
            )
            formatted_response = format_answer(response)

        # Update chat history
        chat_history = update_chat_history(
            chat_id=self.chat_id,
            user_message=question,
            assistant=formatted_response.content or "",
        )

        return chat_history
