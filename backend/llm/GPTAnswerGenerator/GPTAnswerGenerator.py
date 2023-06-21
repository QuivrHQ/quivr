import os  # A module to interact with the OS
from typing import Optional


from typing import Any, Dict, List  # For type hinting
from models.settings import common_dependencies
from langchain.chat_models import ChatOpenAI, ChatVertexAI
from langchain.schema import RUN_KEY, BaseMemory, RunInfo
from repository.chat.get_chat_history import get_chat_history
from .utils.format_answer import format_answer


# Importing various modules and classes from a custom library 'langchain' likely used for natural language processing
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chat_models.anthropic import ChatAnthropic
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings


from langchain.llms import OpenAI, VertexAI
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import SupabaseVectorStore
from llm.prompt import LANGUAGE_PROMPT
from llm.prompt.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT
from models.chats import (
    ChatMessage,
    ChatHistory,
)  # Importing a custom ChatMessage class for handling chat messages
from models.settings import BrainSettings  # Importing settings related to the 'brain'
from pydantic import (
    BaseModel,  # For data validation and settings management
    BaseSettings,
)
from llm.GPTAnswerGenerator.models.FunctionCall import FunctionCall
from llm.GPTAnswerGenerator.models.OpenAiAnswer import OpenAiAnswer

from repository.chat.get_chat_by_id import get_chat_by_id

from supabase import Client, create_client  # For interacting with Supabase database
from vectorstore.supabase import (
    CustomSupabaseVectorStore,
)  # Custom class for handling vector storage with Supabase
from logger import get_logger

logger = get_logger(__name__)


prompt_template = "Your name is Quivr. You are a second brain. A person will ask you a question and you will provide a helpful answer. Write the answer in the same language as the question. If you don't know the answer, just say that you don't know. Don't try to make up an answer."


get_history_schema = {
    "name": "get_history",
    "description": "Get current chat previous messages",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}

get_context_schema = {
    "name": "get_context",
    "description": "Get user documents that is can used for context. It is like it's brain uploaded",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}


class GPTAnswerGenerator:
    # Default class attributes
    model: str = "gpt-3.5-turbo-16k"
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
    ) -> "GPTAnswerGenerator":
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.chat_id = chat_id
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.settings.openai_api_key)
        self.supabase_client = create_client(
            self.settings.supabase_url, self.settings.supabase_service_key
        )
        self.user_email = user_email
        self.openai_client = ChatOpenAI()

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
            messages.append({"role": "user", "content": question})
            return messages

        if useHistory:
            history = self._get_formatted_history()
            if len(history):
                messages.append(
                    {
                        "role": "user",
                        "content": "Here are previous messages:",
                    },
                )
                messages.extend(history)
            else:
                messages.extend(
                    [
                        {
                            "role": "user",
                            "content": "This is the first message of the chat. There is no previous one",
                        },
                    ]
                )

            messages.extend(
                [
                    {
                        "role": "user",
                        "content": f"Question: {question}\n\nAnswer",
                    },
                ]
            )
        if useContext:
            chat_context = self._get_context(question)
            enhanced_question = f"Here is chat context: {chat_context if len(chat_context) else 'No document found'}"
            messages.append({"role": "user", "content": enhanced_question})
            messages.append(
                {
                    "role": "user",
                    "content": f"Question: {question}\n\nAnswer",
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
