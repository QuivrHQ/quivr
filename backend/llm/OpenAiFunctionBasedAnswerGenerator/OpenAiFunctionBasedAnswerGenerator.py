from typing import Optional


from typing import Any, Dict, List  # For type hinting
from langchain.chat_models import ChatOpenAI
from repository.chat.get_chat_history import get_chat_history
from .utils.format_answer import format_answer


# Importing various modules and classes from a custom library 'langchain' likely used for natural language processing
from langchain.embeddings.openai import OpenAIEmbeddings


from models.settings import BrainSettings  # Importing settings related to the 'brain'
from llm.OpenAiFunctionBasedAnswerGenerator.models.OpenAiAnswer import OpenAiAnswer

from supabase import Client, create_client  # For interacting with Supabase database
from vectorstore.supabase import (
    CustomSupabaseVectorStore,
)  # Custom class for handling vector storage with Supabase
from logger import get_logger

logger = get_logger(__name__)

get_context_function_name = "get_context"

prompt_template = """Your name is Quivr. You are a second brain. 
A person will ask you a question and you will provide a helpful answer. 
Write the answer in the same language as the question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Your main goal is to answer questions about user uploaded documents. Unless basic questions or greetings, you should always refer to user uploaded documents by fetching them with the {} function.""".format(
    get_context_function_name
)

get_history_schema = {
    "name": "get_history",
    "description": "Get current chat previous messages",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}

get_context_schema = {
    "name": get_context_function_name,
    "description": "A function which returns user uploaded documents and which must be used when you don't now the answer to a question or when the question seems to refer to user uploaded documents",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}


class OpenAiFunctionBasedAnswerGenerator:
    # Default class attributes
    model: str = "gpt-3.5-turbo-0613"
    temperature: float = 0.0
    max_tokens: int = 256
    chat_id: str
    supabase_client: Client = None
    embeddings: OpenAIEmbeddings = None
    settings = BrainSettings()
    openai_client: ChatOpenAI = None
    user_email: str

    def __init__(
        self,
        model: str,
        chat_id: str,
        temperature: float,
        max_tokens: int,
        user_email: str,
        user_openai_api_key: str,
    ) -> "OpenAiFunctionBasedAnswerGenerator":
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.chat_id = chat_id
        self.supabase_client = create_client(
            self.settings.supabase_url, self.settings.supabase_service_key
        )
        self.user_email = user_email
        if user_openai_api_key is not None:
            self.settings.openai_api_key = user_openai_api_key
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.settings.openai_api_key)
        self.openai_client = ChatOpenAI(openai_api_key=self.settings.openai_api_key)

    def _get_model_response(
        self,
        messages: list[dict[str, str]] = [],
        functions: list[dict[str, Any]] = None,
    ):
        if functions is not None:
            model_response = self.openai_client.completion_with_retry(
                functions=functions,
                messages=messages,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

        else:
            model_response = self.openai_client.completion_with_retry(
                messages=messages,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

        return model_response

    def _get_formatted_history(self) -> List[Dict[str, str]]:
        formatted_history = []
        history = get_chat_history(self.chat_id)
        for chat in history:
            formatted_history.append({"role": "user", "content": chat.user_message})
            formatted_history.append({"role": "assistant", "content": chat.assistant})
        return formatted_history

    def _get_formatted_prompt(
        self,
        question: Optional[str],
        useContext: Optional[bool] = False,
        useHistory: Optional[bool] = False,
    ) -> list[dict[str, str]]:
        messages = [
            {"role": "system", "content": prompt_template},
        ]

        if not useHistory and not useContext:
            messages.append(
                {"role": "user", "content": question},
            )
            return messages

        if useHistory:
            history = self._get_formatted_history()
            if len(history):
                messages.append(
                    {
                        "role": "system",
                        "content": "Previous messages are already in chat.",
                    },
                )
                messages.extend(history)
            else:
                messages.append(
                    {
                        "role": "user",
                        "content": "This is the first message of the chat. There is no previous one",
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nAnswer:",
                }
            )
        if useContext:
            chat_context = self._get_context(question)
            enhanced_question = f"Here is chat context: {chat_context if len(chat_context) else 'No document found'}"
            messages.append({"role": "user", "content": enhanced_question})
            messages.append(
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nAnswer:",
                }
            )
        return messages

    def _get_context(self, question: str) -> str:
        # retrieve 5 nearest documents
        vector_store = CustomSupabaseVectorStore(
            self.supabase_client,
            self.embeddings,
            table_name="vectors",
            user_id=self.user_email,
        )

        return vector_store.similarity_search(
            query=question,
        )

    def _get_answer_from_question(self, question: str) -> OpenAiAnswer:
        functions = [get_history_schema, get_context_schema]

        model_response = self._get_model_response(
            messages=self._get_formatted_prompt(question=question),
            functions=functions,
        )

        return format_answer(model_response)

    def _get_answer_from_question_and_history(self, question: str) -> OpenAiAnswer:
        logger.info("Using chat history")

        functions = [
            get_context_schema,
        ]

        model_response = self._get_model_response(
            messages=self._get_formatted_prompt(question=question, useHistory=True),
            functions=functions,
        )

        return format_answer(model_response)

    def _get_answer_from_question_and_context(self, question: str) -> OpenAiAnswer:
        logger.info("Using documents ")

        functions = [
            get_history_schema,
        ]
        model_response = self._get_model_response(
            messages=self._get_formatted_prompt(question=question, useContext=True),
            functions=functions,
        )

        return format_answer(model_response)

    def _get_answer_from_question_and_context_and_history(
        self, question: str
    ) -> OpenAiAnswer:
        logger.info("Using context and history")
        model_response = self._get_model_response(
            messages=self._get_formatted_prompt(
                question, useContext=True, useHistory=True
            ),
        )
        return format_answer(model_response)

    def get_answer(self, question: str) -> str:
        response = self._get_answer_from_question(question)
        function_name = response.function_call.name if response.function_call else None

        if function_name == "get_history":
            response = self._get_answer_from_question_and_history(question)
        elif function_name == "get_context":
            response = self._get_answer_from_question_and_context(question)

        if response.function_call:
            response = self._get_answer_from_question_and_context_and_history(question)

        return response.content or ""
