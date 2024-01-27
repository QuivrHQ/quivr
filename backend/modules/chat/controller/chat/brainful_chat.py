from llm.api_brain_qa import APIBrainQA
from llm.knowledge_brain_qa import KnowledgeBrainQA
from logger import get_logger
from modules.brain.entity.brain_entity import BrainType, RoleEnum
from modules.brain.service.api_brain_definition_service import ApiBrainDefinitionService
from modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from modules.brain.service.brain_service import BrainService
from modules.chat.controller.chat.interface import ChatInterface
from modules.chat.service.chat_service import ChatService

chat_service = ChatService()
api_brain_definition_service = ApiBrainDefinitionService()

logger = get_logger(__name__)

models_supporting_function_calls = [
    "gpt-4",
    "gpt-4-1106-preview",
    "gpt-4-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0613",
]

brain_service = BrainService()


class BrainfulChat(ChatInterface):
    def validate_authorization(self, user_id, brain_id):
        if brain_id:
            validate_brain_authorization(
                brain_id=brain_id,
                user_id=user_id,
                required_roles=[RoleEnum.Viewer, RoleEnum.Editor, RoleEnum.Owner],
            )

    def get_answer_generator(
        self,
        brain,
        chat_id,
        model,
        max_tokens,
        max_input,
        temperature,
        streaming,
        prompt_id,
        user_id,
        metadata,
    ):
        if (
            brain
            and brain.brain_type == BrainType.DOC
            or model not in models_supporting_function_calls
        ):
            return KnowledgeBrainQA(
                chat_id=chat_id,
                model=model,
                max_tokens=max_tokens,
                max_input=max_input,
                temperature=temperature,
                brain_id=str(brain.brain_id),
                streaming=streaming,
                prompt_id=prompt_id,
                metadata=metadata,
            )

        if brain.brain_type == BrainType.API:
            brain_definition = api_brain_definition_service.get_api_brain_definition(
                brain.brain_id
            )
            return APIBrainQA(
                chat_id=chat_id,
                model=model,
                max_tokens=max_tokens,
                max_input=max_input,
                temperature=temperature,
                brain_id=str(brain.brain_id),
                streaming=streaming,
                prompt_id=prompt_id,
                user_id=user_id,
                metadata=metadata,
                raw=(brain_definition.raw if brain_definition else None),
                jq_instructions=(
                    brain_definition.jq_instructions if brain_definition else None
                ),
            )
