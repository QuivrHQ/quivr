import datetime
import logging
from uuid import UUID, uuid4

from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from quivr_api.models.settings import settings
from quivr_api.modules.brain.service.utils.format_chat_history import (
    format_chat_history,
)
from quivr_api.modules.chat.controller.chat.utils import (
    compute_cost,
    find_model_and_generate_metadata,
    update_user_usage,
)
from quivr_api.modules.chat.dto.inputs import CreateChatHistory
from quivr_api.modules.chat.dto.outputs import GetChatHistoryOutput
from quivr_api.modules.chat.service.chat_service import ChatService
from quivr_api.modules.user.entity.user_identity import UserIdentity
from quivr_api.modules.user.service.user_usage import UserUsage
from quivr_api.packages.quivr_core.models import ParsedRAGResponse, RAGResponseMetadata
from quivr_core.chat import ChatHistory
from quivr_core.models import ParsedRAGResponse, RAGResponseMetadata

logger = logging.getLogger(__name__)


class ChatLLM:
    def __init__(
        self,
        current_user: UserIdentity,
        chat_id: UUID,
        chat_service: ChatService,
        model: str,
    ):
        # Services
        self.chat_service = chat_service

        # Base models
        self.current_user = current_user
        self.chat_id = chat_id
        self.model_to_use = self.check_and_update_user_usage(self.current_user, model)

        # check at init time

    def check_and_update_user_usage(self, user: UserIdentity, model: str):
        """Check user limits and raises if user reached his limits:
        1. Raise if one of the conditions :
           - User doesn't have access to brains
           - Model of brain is not is user_settings.models
           - Latest sum_30d(user_daily_user) < user_settings.max_monthly_usage
           - Check sum(user_settings.daily_user_count)+ model_price <  user_settings.monthly_chat_credits
        2. Updates user usage
        """
        # TODO(@aminediro) : THIS is bug prone, should retrieve it from DB here
        user_usage = UserUsage(id=user.id, email=user.email)
        user_settings = user_usage.get_user_settings()
        all_models = user_usage.get_models()

        # TODO(@aminediro): refactor this function
        model_to_use = find_model_and_generate_metadata(
            model,
            user_settings,
            all_models,
        )
        cost = compute_cost(model_to_use, all_models)
        # Raises HTTP if user usage exceeds limits
        update_user_usage(user_usage, user_settings, cost)  # noqa: F821
        return model_to_use

    def get_llm(self, model: str, streaming: bool):
        api_base = (
            settings.ollama_api_base_url
            if settings.ollama_api_base_url and model.startswith("ollama")
            else None
        )
        return ChatLiteLLM(
            temperature=0.1,
            max_tokens=2000,
            model=model,
            streaming=streaming,
            verbose=False,
            api_base=api_base,
        )  # pyright: ignore reportPrivateUsage=none

    def filter_history(
        self,
        chat_history: ChatHistory,
    ):
        """
        Filter out the chat history to only include the messages that are relevant to the current question
        """
        total_tokens = 0
        total_pairs = 0
        filtered_chat_history: list[AIMessage | HumanMessage] = []
        for human_message, ai_message in chat_history.iter_pairs():
            # TODO: replace with tiktoken
            message_tokens = (len(human_message.content) + len(ai_message.content)) // 4
            if total_tokens + message_tokens > 2000 or total_pairs >= 2000:
                break
            filtered_chat_history.append(human_message)
            filtered_chat_history.append(ai_message)
            total_tokens += message_tokens
            total_pairs += 1

        return filtered_chat_history[::-1]

    def build_chain(self, streaming: bool):

        loaded_memory = RunnablePassthrough.assign(
            chat_history=RunnableLambda(
                lambda x: self.filter_history(x["chat_history"]),
            ),
            question=lambda x: x["question"],
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an assistant.",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        answer = {"answer": prompt | self.get_llm(self.model_to_use.name, streaming)}

        return loaded_memory | answer

    async def generate_answer(
        self,
        question: str,
    ):

        history = await self.chat_service.get_chat_history(self.chat_id)
        # Get list of files
        llm = self.get_llm(self.model_to_use.name, False)
        # Initialize the RAG pipline
        #  Format the history, sanitize the input
        transformed_history = format_chat_history(history)

        chain = self.build_chain(False)

        parsed_response = chain.invoke({"question": question})

        # Save the answer to db
        new_chat_entry = self.save_answer(question, parsed_response)

        # Format output to be correct
        return GetChatHistoryOutput(
            **{
                "chat_id": self.chat_id,
                "user_message": question,
                "assistant": parsed_response.answer,
                "message_time": new_chat_entry.message_time,
                "prompt_title": None,
                "brain_name": None,
                "message_id": new_chat_entry.message_id,
                "brain_id": None,
                "metadata": {},
            }
        )

    async def generate_answer_stream(
        self,
        question: str,
    ):

        # Getting chat history
        history = await self.chat_service.get_chat_history(self.chat_id)
        #  Format the history, sanitize the input
        transformed_history = format_chat_history(history)

        chain = self.build_chain(True)

        full_answer = ""

        message_metadata = {
            "chat_id": self.chat_id,
            "message_id": uuid4(),  # do we need it ?,
            "user_message": question,  # TODO: define result
            "message_time": datetime.datetime.now(),  # TODO: define result
            "prompt_title": None,
            "brain_name": None,
            "brain_id": None,
        }

        async for response in chain.answer_astream(question, transformed_history):
            # Format output to be correct servicedf;j
            if not response.last_chunk:
                streamed_chat_history = GetChatHistoryOutput(
                    assistant=response.answer,
                    metadata=response.metadata.model_dump(),
                    **message_metadata,
                )
                full_answer += response.answer
                yield f"data: {streamed_chat_history.model_dump_json()}"

        # For last chunk  parse the sources, and the full answer
        streamed_chat_history = GetChatHistoryOutput(
            assistant=response.answer,
            metadata=response.metadata.model_dump(),
            **message_metadata,
        )

        self.save_answer(
            question,
            ParsedRAGResponse(
                answer=full_answer,
                metadata=RAGResponseMetadata(**streamed_chat_history.metadata),
            ),
        )
        yield f"data: {streamed_chat_history.model_dump_json()}"

    def save_answer(self, question: str, answer: ParsedRAGResponse):
        return self.chat_service.update_chat_history(
            CreateChatHistory(
                **{
                    "chat_id": self.chat_id,
                    "user_message": question,
                    "assistant": answer.answer,
                    "brain_id": None,
                    # TODO: prompt_id should always be not None
                    "prompt_id": None,
                    "metadata": {},
                }
            )
        )
