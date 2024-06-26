import datetime
from typing import Type
from uuid import UUID, uuid4

from backend.logger import get_logger
from backend.models.settings import get_embedding_client, get_supabase_client
from backend.modules.brain.entity.brain_entity import BrainEntity
from backend.modules.brain.entity.integration_brain import IntegrationEntity
from backend.modules.brain.integrations.Big.Brain import BigBrain
from backend.modules.brain.integrations.GPT4.Brain import GPT4Brain
from backend.modules.brain.integrations.Multi_Contract.Brain import MultiContractBrain
from backend.modules.brain.integrations.Notion.Brain import NotionBrain
from backend.modules.brain.integrations.Proxy.Brain import ProxyBrain
from backend.modules.brain.integrations.Self.Brain import SelfBrain
from backend.modules.brain.integrations.SQL.Brain import SQLBrain
from backend.modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from backend.modules.brain.service.brain_service import BrainService
from backend.modules.brain.service.utils.format_chat_history import format_chat_history
from backend.modules.chat.controller.chat.utils import (
    compute_cost,
    find_model_and_generate_metadata,
    update_user_usage,
)
from backend.modules.chat.dto.inputs import CreateChatHistory
from backend.modules.chat.dto.outputs import GetChatHistoryOutput
from backend.modules.chat.service.chat_service import ChatService
from backend.modules.knowledge.repository.knowledges import KnowledgeRepository
from backend.modules.prompt.entity.prompt import Prompt
from backend.modules.prompt.service.prompt_service import PromptService
from backend.modules.user.entity.user_identity import UserIdentity
from backend.modules.user.service.user_usage import UserUsage
from backend.packages.quivr_core.config import RAGConfig
from backend.packages.quivr_core.models import ParsedRAGResponse, RAGResponseMetadata
from backend.packages.quivr_core.quivr_rag import QuivrQARAG
from backend.packages.quivr_core.utils import generate_source
from backend.vectorstore.supabase import CustomSupabaseVectorStore

logger = get_logger(__name__)


class RAGServiceFactory:
    integration_list: dict[str, Type[KnowledgeBrainQA]] = {
        "notion": NotionBrain,
        "gpt4": GPT4Brain,
        "sql": SQLBrain,
        "big": BigBrain,
        "doc": KnowledgeBrainQA,
        "proxy": ProxyBrain,
        "self": SelfBrain,
        "multi-contract": MultiContractBrain,
    }

    def get_brain_cls(self, integration: IntegrationEntity):
        pass


class RAGService:
    def __init__(
        self,
        current_user: UserIdentity,
        brain_id: UUID | None,
        chat_id: UUID,
        brain_service: BrainService,
        prompt_service: PromptService,
        chat_service: ChatService,
        knowledge_service: KnowledgeRepository,
    ):
        # Services
        self.brain_service = brain_service
        self.prompt_service = prompt_service
        self.chat_service = chat_service
        self.knowledge_service = knowledge_service

        # Base models
        self.current_user = current_user
        self.chat_id = chat_id
        self.brain = self.get_or_create_brain(brain_id, self.current_user.id)
        self.prompt = self.get_brain_prompt(self.brain)

        # check at init time
        self.model_to_use = self.check_and_update_user_usage(
            self.current_user, self.brain
        )

    def get_brain_prompt(self, brain: BrainEntity) -> Prompt | None:
        return (
            self.prompt_service.get_prompt_by_id(brain.prompt_id)
            if brain.prompt_id
            else None
        )

    def get_or_create_brain(self, brain_id: UUID | None, user_id: UUID) -> BrainEntity:
        brain = None
        if brain_id is not None:
            brain = self.brain_service.get_brain_details(brain_id, user_id)

        else:
            brain = self.brain_service.create_or_get_quivr_brain(user_id)

        # if brain.integration:
        #     assert brain.integration.user_id == user_id
        return brain

    def check_and_update_user_usage(self, user: UserIdentity, brain: BrainEntity):
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
            brain.model,
            user_settings,
            all_models,
        )
        cost = compute_cost(model_to_use, all_models)
        # Raises HTTP if user usage exceeds limits
        update_user_usage(user_usage, user_settings, cost)  # noqa: F821
        return model_to_use

    def create_vector_store(
        self, brain_id: UUID, max_input: int
    ) -> CustomSupabaseVectorStore:
        supabase_client = get_supabase_client()
        embeddings = get_embedding_client()
        return CustomSupabaseVectorStore(
            supabase_client,
            embeddings,
            table_name="vectors",
            brain_id=brain_id,
            max_input=max_input,
        )

    def save_answer(self, question: str, answer: ParsedRAGResponse):
        return self.chat_service.update_chat_history(
            CreateChatHistory(
                **{
                    "chat_id": self.chat_id,
                    "user_message": question,
                    "assistant": answer.answer,
                    "brain_id": self.brain.brain_id,
                    # TODO: prompt_id should always be not None
                    "prompt_id": self.prompt.id if self.prompt else None,
                    "metadata": answer.metadata.model_dump() if answer.metadata else {},
                }
            )
        )

    async def generate_answer(
        self,
        question: str,
    ):
        logger.info(
            f"Creating question for chat {self.chat_id} with brain {self.brain.brain_id} "
        )
        rag_config = RAGConfig(
            model=self.model_to_use.name,
            temperature=self.brain.temperature,
            max_input=self.model_to_use.max_input,
            max_tokens=self.brain.max_tokens,
            prompt=self.prompt.content if self.prompt else None,
            streaming=False,
        )
        history = await self.chat_service.get_chat_history(self.chat_id)
        # Get list of files
        list_files = self.knowledge_service.get_all_knowledge_in_brain(
            self.brain.brain_id
        )
        vector_store = self.create_vector_store(
            self.brain.brain_id, rag_config.max_input
        )
        # Initialize the rag pipline
        rag_pipeline = QuivrQARAG(rag_config, vector_store)
        #  Format the history, sanitize the input
        transformed_history = format_chat_history(history)

        parsed_response = rag_pipeline.answer(question, transformed_history, list_files)

        # Save the answer to db
        new_chat_entry = self.save_answer(question, parsed_response)

        # Format output to be correct
        return GetChatHistoryOutput(
            **{
                "chat_id": self.chat_id,
                "user_message": question,
                "assistant": parsed_response.answer,
                "message_time": new_chat_entry.message_time,
                "prompt_title": (self.prompt.title if self.prompt else None),
                "brain_name": self.brain.name if self.brain else None,
                "message_id": new_chat_entry.message_id,
                "brain_id": str(self.brain.brain_id) if self.brain else None,
                "metadata": (
                    parsed_response.metadata.model_dump()
                    if parsed_response.metadata
                    else {}
                ),
            }
        )

    async def generate_answer_stream(
        self,
        question: str,
    ):
        logger.info(
            f"Creating question for chat {self.chat_id} with brain {self.brain.brain_id} "
        )
        # Build the rag config
        rag_config = RAGConfig(
            model=self.model_to_use.name,
            temperature=self.brain.temperature,
            max_input=self.model_to_use.max_input,
            max_tokens=self.brain.max_tokens,
            prompt=self.prompt.content if self.prompt else "",
            streaming=True,
        )
        # Getting chat history
        history = await self.chat_service.get_chat_history(self.chat_id)
        #  Format the history, sanitize the input
        transformed_history = format_chat_history(history)

        # Get list of files urls
        # TODO: Why do we get ALL the files ?
        list_files = self.knowledge_service.get_all_knowledge_in_brain(
            self.brain.brain_id
        )
        vector_store = self.create_vector_store(
            self.brain.brain_id, rag_config.max_input
        )
        # Initialize the rag pipline
        rag_pipeline = QuivrQARAG(rag_config, vector_store)

        full_answer = ""

        message_metadata = {
            "chat_id": self.chat_id,
            "message_id": uuid4(),  # do we need it ?,
            "user_message": question,  # TODO: define result
            "message_time": datetime.datetime.now(),  # TODO: define result
            "prompt_title": (self.prompt.title if self.prompt else ""),
            "brain_name": self.brain.name if self.brain else None,
            "brain_id": self.brain.brain_id if self.brain else None,
        }

        async for response in rag_pipeline.answer_astream(
            question, transformed_history, list_files
        ):
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

        sources_urls = generate_source(
            response.metadata.sources,
            self.brain.brain_id,
            (
                streamed_chat_history.metadata["citations"]
                if streamed_chat_history.metadata
                else None
            ),
        )
        if streamed_chat_history.metadata:
            streamed_chat_history.metadata["sources"] = sources_urls

        self.save_answer(
            question,
            ParsedRAGResponse(
                answer=full_answer,
                metadata=RAGResponseMetadata(**streamed_chat_history.metadata),
            ),
        )
        yield f"data: {streamed_chat_history.model_dump_json()}"