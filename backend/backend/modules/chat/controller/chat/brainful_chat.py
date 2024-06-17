from backend.logger import get_logger
from backend.modules.brain.entity.brain_entity import BrainType, RoleEnum
from backend.modules.brain.integrations.Big.Brain import BigBrain
from backend.modules.brain.integrations.GPT4.Brain import GPT4Brain
from backend.modules.brain.integrations.Multi_Contract.Brain import MultiContractBrain
from backend.modules.brain.integrations.Notion.Brain import NotionBrain
from backend.modules.brain.integrations.Proxy.Brain import ProxyBrain
from backend.modules.brain.integrations.Self.Brain import SelfBrain
from backend.modules.brain.integrations.SQL.Brain import SQLBrain
from backend.modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from backend.modules.brain.service.api_brain_definition_service import (
    ApiBrainDefinitionService,
)
from backend.modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from backend.modules.brain.service.brain_service import BrainService
from backend.modules.brain.service.integration_brain_service import (
    IntegrationBrainDescriptionService,
)
from backend.modules.chat.controller.chat.interface import ChatInterface
from backend.modules.chat.service.chat_service import ChatService
from backend.modules.dependencies import get_service

chat_service = get_service(ChatService)()
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
    "gpt-4-turbo",
    "gpt-4o",
]


integration_list = {
    "notion": NotionBrain,
    "gpt4": GPT4Brain,
    "sql": SQLBrain,
    "big": BigBrain,
    "doc": KnowledgeBrainQA,
    "proxy": ProxyBrain,
    "self": SelfBrain,
    "multi-contract": MultiContractBrain,
}

brain_service = BrainService()


def validate_authorization(user_id, brain_id):
    if brain_id:
        validate_brain_authorization(
            brain_id=brain_id,
            user_id=user_id,
            required_roles=[RoleEnum.Viewer, RoleEnum.Editor, RoleEnum.Owner],
        )


# TODO: redo this
class BrainfulChat(ChatInterface):
    def get_answer_generator(
        self,
        brain,
        chat_id,
        chat_service,
        model,
        temperature,
        streaming,
        prompt_id,
        user_id,
        user_email,
    ):
        if brain and brain.brain_type == BrainType.doc:
            return KnowledgeBrainQA(
                chat_service=chat_service,
                chat_id=chat_id,
                brain_id=str(brain.brain_id),
                streaming=streaming,
                prompt_id=prompt_id,
                user_id=user_id,
                user_email=user_email,
            )

        if brain.brain_type == BrainType.integration:
            integration_brain = integration_brain_description_service.get_integration_description_by_user_brain_id(
                brain.brain_id, user_id
            )

            integration_class = integration_list.get(
                integration_brain.integration_name.lower()
            )
            if integration_class:
                return integration_class(
                    chat_service=chat_service,
                    chat_id=chat_id,
                    temperature=temperature,
                    brain_id=str(brain.brain_id),
                    streaming=streaming,
                    prompt_id=prompt_id,
                    user_id=user_id,
                    user_email=user_email,
                )
