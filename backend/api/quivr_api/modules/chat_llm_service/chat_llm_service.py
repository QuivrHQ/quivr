import datetime
import os
from uuid import UUID, uuid4

from quivr_core.chat import ChatHistory as ChatHistoryCore
from quivr_core.chat_llm import ChatLLM
from quivr_core.config import LLMEndpointConfig
from quivr_core.llm.llm_endpoint import LLMEndpoint
from quivr_core.models import ChatLLMMetadata, ParsedRAGResponse, RAGResponseMetadata

from quivr_api.logger import get_logger
from quivr_api.modules.brain.service.utils.format_chat_history import (
    format_chat_history,
)
from quivr_api.modules.chat.dto.inputs import CreateChatHistory
from quivr_api.modules.chat.dto.outputs import GetChatHistoryOutput
from quivr_api.modules.chat.service.chat_service import ChatService
from quivr_api.modules.models.service.model_service import ModelService
from quivr_api.modules.user.entity.user_identity import UserIdentity
from quivr_api.packages.utils.uuid_generator import generate_uuid_from_string

logger = get_logger(__name__)


class ChatLLMService:
    def __init__(
        self,
        current_user: UserIdentity,
        model_name: str,
        chat_id: UUID,
        chat_service: ChatService,
        model_service: ModelService,
    ):
        # Services
        self.chat_service = chat_service
        self.model_service = model_service

        # Base models
        self.current_user = current_user
        self.chat_id = chat_id

        # check at init time
        self.model_to_use = model_name

    def _build_chat_history(
        self,
        history: list[GetChatHistoryOutput],
    ) -> ChatHistoryCore:
        transformed_history = format_chat_history(history)
        chat_history = ChatHistoryCore(brain_id=None, chat_id=self.chat_id)

        [chat_history.append(m) for m in transformed_history]
        return chat_history

    async def build_llm(self) -> ChatLLM:
        model = await self.model_service.get_model(self.model_to_use)
        api_key = os.getenv(model.env_variable_name, "not-defined")
        chat_llm = ChatLLM(
            llm=LLMEndpoint.from_config(
                LLMEndpointConfig(
                    model=self.model_to_use,
                    llm_base_url=model.endpoint_url,
                    llm_api_key=api_key,
                    temperature=(LLMEndpointConfig.model_fields["temperature"].default),
                    max_input=model.max_input,
                    max_tokens=model.max_output,
                ),
            )
        )
        return chat_llm

    def save_answer(self, question: str, answer: ParsedRAGResponse):
        logger.info(
            f"Saving answer for chat {self.chat_id} with model {self.model_to_use}"
        )
        logger.info(answer)
        return self.chat_service.update_chat_history(
            CreateChatHistory(
                **{
                    "chat_id": self.chat_id,
                    "user_message": question,
                    "assistant": answer.answer,
                    "brain_id": None,
                    "prompt_id": None,
                    "metadata": answer.metadata.model_dump() if answer.metadata else {},
                }
            )
        )

    async def generate_answer(
        self,
        question: str,
    ):
        logger.info(
            f"Creating question for chat {self.chat_id} with model {self.model_to_use} "
        )
        chat_llm = await self.build_llm()
        history = await self.chat_service.get_chat_history(self.chat_id)
        model_metadata = await self.model_service.get_model(self.model_to_use)
        #  Format the history, sanitize the input
        chat_history = self._build_chat_history(history)

        parsed_response = chat_llm.answer(question, chat_history)

        if parsed_response.metadata:
            # TODO: check if this is the right way to do it
            parsed_response.metadata.metadata_model = ChatLLMMetadata(
                name=self.model_to_use,
                description=model_metadata.description,
                image_url=model_metadata.image_url,
                display_name=model_metadata.display_name,
                brain_id=str(generate_uuid_from_string(self.model_to_use)),
                brain_name=self.model_to_use,
            )

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
            f"Creating question for chat {self.chat_id} with model {self.model_to_use} "
        )
        # Build the rag config
        chat_llm = await self.build_llm()

        # Get model metadata
        model_metadata = await self.model_service.get_model(self.model_to_use)
        # Get chat history
        history = await self.chat_service.get_chat_history(self.chat_id)
        #  Format the history, sanitize the input
        chat_history = self._build_chat_history(history)

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
        metadata_model = ChatLLMMetadata(
            name=self.model_to_use,
            description=model_metadata.description,
            image_url=model_metadata.image_url,
            display_name=model_metadata.display_name,
            brain_id=str(generate_uuid_from_string(self.model_to_use)),
            brain_name=self.model_to_use,
        )

        async for response in chat_llm.answer_astream(question, chat_history):
            # Format output to be correct servicedf;j
            if not response.last_chunk:
                streamed_chat_history = GetChatHistoryOutput(
                    assistant=response.answer,
                    metadata=response.metadata.model_dump(),
                    **message_metadata,
                )
                streamed_chat_history.metadata["metadata_model"] = metadata_model  # type: ignore
                full_answer += response.answer
                yield f"data: {streamed_chat_history.model_dump_json()}"
            if response.last_chunk and full_answer == "":
                full_answer += response.answer

        # For last chunk  parse the sources, and the full answer
        streamed_chat_history = GetChatHistoryOutput(
            assistant="",
            metadata=response.metadata.model_dump(),
            **message_metadata,
        )

        metadata = RAGResponseMetadata(**streamed_chat_history.metadata)  # type: ignore
        metadata.metadata_model = ChatLLMMetadata(
            name=self.model_to_use,
            description=model_metadata.description,
            image_url=model_metadata.image_url,
            display_name=model_metadata.display_name,
            brain_id=str(generate_uuid_from_string(self.model_to_use)),
            brain_name=self.model_to_use,
        )
        streamed_chat_history.metadata = metadata.model_dump()

        logger.info("Last chunk before saving")
        self.save_answer(
            question,
            ParsedRAGResponse(
                answer=full_answer,
                metadata=metadata,
            ),
        )
        yield f"data: {streamed_chat_history.model_dump_json()}"
