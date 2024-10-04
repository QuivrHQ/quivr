import datetime
import os
from uuid import UUID, uuid4

from quivr_core.brain import Brain as BrainCore
from quivr_core.chat import ChatHistory as ChatHistoryCore
from quivr_core.config import LLMEndpointConfig, RetrievalConfig
from quivr_core.llm.llm_endpoint import LLMEndpoint
from quivr_core.models import ChatLLMMetadata, ParsedRAGResponse, RAGResponseMetadata
from quivr_core.quivr_rag_langgraph import QuivrQARAGLangGraph

from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import BrainEntity
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.utils.format_chat_history import (
    format_chat_history,
)
from quivr_api.modules.chat.dto.inputs import CreateChatHistory
from quivr_api.modules.chat.dto.outputs import GetChatHistoryOutput
from quivr_api.modules.chat.service.chat_service import ChatService
from quivr_api.modules.dependencies import (
    get_embedding_client,
    get_supabase_client,
)
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.models.service.model_service import ModelService
from quivr_api.modules.prompt.entity.prompt import Prompt
from quivr_api.modules.prompt.service.prompt_service import PromptService
from quivr_api.modules.user.entity.user_identity import UserIdentity
from quivr_api.modules.vector.service.vector_service import VectorService
from quivr_api.utils.uuid_generator import generate_uuid_from_string
from quivr_api.vectorstore.supabase import CustomSupabaseVectorStore

from .utils import generate_source

logger = get_logger(__name__)


class RAGService:
    def __init__(
        self,
        current_user: UserIdentity,
        chat_id: UUID,
        model_service: ModelService,
        chat_service: ChatService,
        brain: BrainEntity,
        retrieval_config: RetrievalConfig | None = None,
        brain_service: BrainService | None = None,
        prompt_service: PromptService | None = None,
        knowledge_service: KnowledgeService | None = None,
        vector_service: VectorService | None = None,
    ):
        # Services
        self.brain_service = brain_service
        self.prompt_service = prompt_service
        self.chat_service = chat_service
        self.knowledge_service = knowledge_service
        self.vector_service = vector_service
        self.model_service = model_service

        # Base models
        self.current_user = current_user
        self.chat_id = chat_id
        self.brain = brain
        self.prompt = (
            self.get_brain_prompt(self.brain)
            if self.brain and self.brain_service
            else None
        )

        self.retrieval_config = retrieval_config

        # check at init time
        self.model_to_use = brain.model if brain else None

    def get_brain_prompt(self, brain: BrainEntity) -> Prompt | None:
        if not self.prompt_service:
            raise ValueError("PromptService not provided")

        return (
            self.prompt_service.get_prompt_by_id(brain.prompt_id)
            if brain.prompt_id
            else None
        )

    def _build_chat_history(
        self,
        history: list[GetChatHistoryOutput],
    ) -> ChatHistoryCore:
        transformed_history = format_chat_history(history)
        chat_history = ChatHistoryCore(
            brain_id=self.brain.brain_id, chat_id=self.chat_id
        )

        [chat_history.append(m) for m in transformed_history]
        return chat_history

    async def _get_retrieval_config(self) -> RetrievalConfig:
        if self.retrieval_config:
            retrieval_config = self.retrieval_config
        else:
            retrieval_config = await self._build_retrieval_config()

        return retrieval_config

    async def _build_retrieval_config(self) -> RetrievalConfig:
        model = await self.model_service.get_model(self.model_to_use)  # type: ignore
        if model is None:
            raise ValueError(f"Cannot get model {self.model_to_use}")
        api_key = os.getenv(model.env_variable_name, "not-defined")

        retrieval_config = RetrievalConfig(
            llm_config=LLMEndpointConfig(
                model=self.model_to_use,  # type: ignore
                llm_base_url=model.endpoint_url,
                llm_api_key=api_key,
                temperature=(LLMEndpointConfig.model_fields["temperature"].default),
                max_input_tokens=model.max_input,
                max_output_tokens=model.max_output,
            ),
            prompt=self.prompt.content if self.prompt else None,
        )
        return retrieval_config

    def get_llm(self, retrieval_config: RetrievalConfig):
        return LLMEndpoint.from_config(retrieval_config.llm_config)

    def create_vector_store(
        self, brain_id: UUID, max_input: int
    ) -> CustomSupabaseVectorStore:
        if not self.vector_service:
            raise ValueError("VectorService not provided")

        supabase_client = get_supabase_client()
        embeddings = get_embedding_client()
        return CustomSupabaseVectorStore(
            supabase_client,
            embeddings,
            table_name="vectors",
            brain_id=brain_id,
            max_input=max_input,
            vector_service=self.vector_service,
        )

    def save_answer(self, question: str, answer: ParsedRAGResponse):
        metadata = answer.metadata.model_dump() if answer.metadata else {}
        metadata["snippet_color"] = self.brain.snippet_color if self.brain else None
        metadata["snippet_emoji"] = self.brain.snippet_emoji if self.brain else None
        logger.info(f"Saving answer with metadata: {metadata}")
        return self.chat_service.update_chat_history(
            CreateChatHistory(
                **{
                    "chat_id": self.chat_id,
                    "user_message": question,
                    "assistant": answer.answer,
                    "brain_id": self.brain.brain_id,
                    # TODO: prompt_id should always be not None
                    "prompt_id": self.prompt.id if self.prompt else None,
                    "metadata": metadata,
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
        retrieval_config = await self._get_retrieval_config()
        logger.debug(f"generate_answer with config : {retrieval_config.model_dump()}")
        history = await self.chat_service.get_chat_history(self.chat_id)
        #  Format the history, sanitize the input
        chat_history = self._build_chat_history(history)

        # Get list of files
        list_files = (
            await self.knowledge_service.get_all_knowledge_in_brain(self.brain.brain_id)
            if self.knowledge_service
            else []
        )

        # Build RAG dependencies to inject
        vector_store = (
            self.create_vector_store(
                self.brain.brain_id, retrieval_config.llm_config.max_input_tokens
            )
            if self.vector_service
            else None
        )

        llm = self.get_llm(retrieval_config)

        brain_core = BrainCore(
            name=self.brain.name,
            id=self.brain.id,
            llm=llm,
            vector_db=vector_store,
            embedder=vector_store.embeddings if vector_store else None,
        )

        parsed_response = brain_core.ask(
            question=question,
            retrieval_config=retrieval_config,
            rag_pipeline=QuivrQARAGLangGraph,
            list_files=list_files,
            chat_history=chat_history,
        )

        # Save the answer to db
        if self.brain_service:
            new_chat_entry = self.save_answer(question, parsed_response)

        # Format output to be correct
        metadata = (
            parsed_response.metadata.model_dump() if parsed_response.metadata else {}
        )
        metadata["snippet_color"] = self.brain.snippet_color if self.brain else None
        metadata["snippet_emoji"] = self.brain.snippet_emoji if self.brain else None
        return GetChatHistoryOutput(
            **{
                "chat_id": self.chat_id,
                "user_message": question,
                "assistant": parsed_response.answer,
                "message_time": new_chat_entry.message_time if new_chat_entry else None,
                "prompt_title": (self.prompt.title if self.prompt else None),
                "brain_name": self.brain.name if self.brain else None,
                "message_id": new_chat_entry.message_id if new_chat_entry else None,
                "brain_id": str(self.brain.brain_id) if self.brain else None,
                "metadata": metadata,
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
        retrieval_config = await self._get_retrieval_config()
        # Get chat history
        history = await self.chat_service.get_chat_history(self.chat_id)
        #  Format the history, sanitize the input
        chat_history = self._build_chat_history(history)

        # Get list of files urls
        list_files = (
            await self.knowledge_service.get_all_knowledge_in_brain(self.brain.brain_id)
            if self.knowledge_service
            else []
        )

        vector_store = (
            self.create_vector_store(
                self.brain.brain_id, retrieval_config.llm_config.max_input_tokens
            )
            if self.vector_service
            else None
        )

        llm = self.get_llm(retrieval_config)

        if self.prompt:
            retrieval_config.prompt = self.prompt.content

        # Get model metadata
        model_metadata = await self.model_service.get_model(self.brain.name)

        brain_core = BrainCore(
            name=self.brain.name,
            id=self.brain.id,
            llm=llm,
            vector_db=vector_store,
            embedder=vector_store.embeddings if vector_store else None,
        )

        full_answer = ""

        metadata = {}
        metadata["snippet_color"] = self.brain.snippet_color if self.brain else None
        metadata["snippet_emoji"] = self.brain.snippet_emoji if self.brain else None
        message_metadata = {
            "chat_id": self.chat_id,
            "message_id": uuid4(),  # do we need it ?,
            "user_message": question,  # TODO: define result
            "message_time": datetime.datetime.now(),  # TODO: define result
            "prompt_title": (self.prompt.title if self.prompt else ""),
            # brain_name and brain_id must be None in the chat-with-llm case, as this will force the front to look for the model_metadata
            "brain_name": self.brain.name if self.brain_service else None,
            "brain_id": self.brain.brain_id if self.brain_service else None,
        }

        metadata_model = {}
        if model_metadata:
            metadata_model = ChatLLMMetadata(
                name=self.brain.name,
                description=model_metadata.description,
                image_url=model_metadata.image_url,
                display_name=model_metadata.display_name,
                brain_id=str(generate_uuid_from_string(self.brain.name)),
                brain_name=self.model_to_use,
            )

        async for response in brain_core.ask_streaming(
            question=question,
            retrieval_config=retrieval_config,
            rag_pipeline=QuivrQARAGLangGraph,
            chat_history=chat_history,
            list_files=list_files,
        ):
            # Format output to be correct servicedf;j
            if not response.last_chunk:
                streamed_chat_history = GetChatHistoryOutput(
                    assistant=response.answer,
                    metadata=response.metadata.model_dump(),
                    **message_metadata,
                )
                if streamed_chat_history.metadata:
                    streamed_chat_history.metadata["snippet_color"] = (
                        self.brain.snippet_color if self.brain else None
                    )
                    streamed_chat_history.metadata["snippet_emoji"] = (
                        self.brain.snippet_emoji if self.brain else None
                    )
                    if metadata_model:
                        streamed_chat_history.metadata["metadata_model"] = (
                            metadata_model
                        )
                full_answer += response.answer
                yield f"data: {streamed_chat_history.model_dump_json()}"

        # For last chunk  parse the sources, and the full answer
        streamed_chat_history = GetChatHistoryOutput(
            assistant=response.answer,
            metadata=response.metadata.model_dump(),
            **message_metadata,
        )

        if streamed_chat_history.metadata:
            streamed_chat_history.metadata["snippet_color"] = (
                self.brain.snippet_color if self.brain else None
            )
            streamed_chat_history.metadata["snippet_emoji"] = (
                self.brain.snippet_emoji if self.brain else None
            )
            if metadata_model:
                streamed_chat_history.metadata["metadata_model"] = metadata_model

        sources_urls = (
            await generate_source(
                knowledge_service=self.knowledge_service,
                brain_id=self.brain.brain_id,
                source_documents=response.metadata.sources,
                citations=(
                    streamed_chat_history.metadata["citations"]
                    if streamed_chat_history.metadata
                    else None
                ),
            )
            if self.knowledge_service
            else []
        )

        if streamed_chat_history.metadata:
            streamed_chat_history.metadata["sources"] = sources_urls

        self.save_answer(
            question,
            ParsedRAGResponse(
                answer=full_answer,
                metadata=RAGResponseMetadata.model_validate(
                    streamed_chat_history.metadata
                ),
            ),
        )
        yield f"data: {streamed_chat_history.model_dump_json()}"
