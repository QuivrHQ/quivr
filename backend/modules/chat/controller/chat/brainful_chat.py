from logger import get_logger
from modules.brain.api_brain_qa import APIBrainQA
from modules.brain.entity.brain_entity import BrainType, RoleEnum
from modules.brain.integrations.Big.Brain import BigBrain
from modules.brain.integrations.GPT4.Brain import GPT4Brain
from modules.brain.integrations.Notion.Brain import NotionBrain
from modules.brain.integrations.SQL.Brain import SQLBrain
from modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from modules.brain.service.api_brain_definition_service import ApiBrainDefinitionService
from modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from modules.brain.service.brain_service import BrainService
from modules.brain.service.integration_brain_service import (
    IntegrationBrainDescriptionService,
)
from modules.chat.controller.chat.interface import ChatInterface
from modules.chat.service.chat_service import ChatService

chat_service = ChatService()
api_brain_definition_service = ApiBrainDefinitionService()
integration_brain_description_service = IntegrationBrainDescriptionService()

logger = get_logger(__name__)

models_supporting_function_calls = [
    "gpt-4",
    "gpt-4-1106-preview",
    "gpt-4-0613",
    "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0613",
    "gpt-4-0125-preview",
    "gpt-3.5-turbo",
]


integration_list = {
    "notion": NotionBrain,
    "gpt4": GPT4Brain,
    "sql": SQLBrain,
    "big": BigBrain,
}

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
        temperature,
        streaming,
        prompt_id,
        user_id,
        user_email,
    ):
        if brain and brain.brain_type == BrainType.DOC:
            return KnowledgeBrainQA(
                chat_id=chat_id,
                brain_id=str(brain.brain_id),
                streaming=streaming,
                prompt_id=prompt_id,
                user_id=user_id,
                user_email=user_email,
            )

        if brain.brain_type == BrainType.API:
            brain_definition = api_brain_definition_service.get_api_brain_definition(
                brain.brain_id
            )
            return APIBrainQA(
                chat_id=chat_id,
                temperature=temperature,
                brain_id=str(brain.brain_id),
                streaming=streaming,
                prompt_id=prompt_id,
                user_id=user_id,
                raw=(brain_definition.raw if brain_definition else None),
                jq_instructions=(
                    brain_definition.jq_instructions if brain_definition else None
                ),
                user_email=user_email,
            )
        if brain.brain_type == BrainType.INTEGRATION:
            integration_brain = integration_brain_description_service.get_integration_description_by_user_brain_id(
                brain.brain_id, user_id
            )

            integration_class = integration_list.get(
                integration_brain.integration_name.lower()
            )
            if integration_class:
                return integration_class(
                    chat_id=chat_id,
                    temperature=temperature,
                    brain_id=str(brain.brain_id),
                    streaming=streaming,
                    prompt_id=prompt_id,
                    user_id=user_id,
                    user_email=user_email,
                )
