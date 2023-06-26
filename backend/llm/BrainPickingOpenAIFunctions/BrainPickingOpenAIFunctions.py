from typing import Any, Dict, List, Optional

from langchain.chat_models import ChatOpenAI
from llm.brainpicking import BrainPicking
from logger import get_logger
from repository.chat.get_chat_history import get_chat_history
from vectorstore.supabase import CustomSupabaseVectorStore

from .utils.format_answer import format_answer

logger = get_logger(__name__)


class BrainPickingOpenAIFunctions(BrainPicking):
    DEFAULT_MODEL = "gpt-3.5-turbo-0613"
    DEFAULT_TEMPERATURE = 0.0
    DEFAULT_MAX_TOKENS = 256

    openai_client: ChatOpenAI = None
    user_email: str = None

    def __init__(
        self,
        model: str,
        chat_id: str,
        temperature: float,
        max_tokens: int,
        user_email: str,
        user_openai_api_key: str,
    ) -> None:
        # Call the constructor of the parent class (BrainPicking)
        super().__init__(
            model=model,
            user_id=user_email,
            chat_id=chat_id,
            max_tokens=max_tokens,
            user_openai_api_key=user_openai_api_key,
            temperature=temperature,
        )
        self.openai_client = ChatOpenAI(openai_api_key=self.settings.openai_api_key)
        self.user_email = user_email

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
            "model": self.llm_name,
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
        vector_store = CustomSupabaseVectorStore(
            self.supabase_client,
            self.embeddings,
            table_name="vectors",
            user_id=self.user_email,
        )

        return vector_store.similarity_search(query=question)

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
                "content": "Your name is Quivr. You are a second brain. A person will ask you a question and you will provide a helpful answer. Write the answer in the same language as the question.If you don't know the answer, just say that you don't know. Don't try to make up an answer.our main goal is to answer questions about user uploaded documents. Unless basic questions or greetings, you should always refer to user uploaded documents by fetching them with the get_context function.",
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

    def generate_answer(self, question: str) -> str:
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
                "name": "get_context",
                "description": "Used for retrieving documents related to the question to help answer the question",
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

        # If the model calls for context, try again with context included
        if (
            formatted_response.function_call
            and formatted_response.function_call.name == "get_context"
        ):
            logger.info("Model called for context")
            response = self._get_model_response(
                messages=self._construct_prompt(
                    question, useContext=True, useHistory=False
                ),
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

        return formatted_response.content or ""
