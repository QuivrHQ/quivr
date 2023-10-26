from llm.qa_base import QABaseBrainPicking
from routes.authorizations.brain_authorization import validate_brain_authorization
from routes.authorizations.types import RoleEnum
from routes.chat.interface import ChatInterface

from repository.brain import get_brain_details


class BrainfulChat(ChatInterface):
    def validate_authorization(self, user_id, brain_id):
        if brain_id:
            validate_brain_authorization(
                brain_id=brain_id,
                user_id=user_id,
                required_roles=[RoleEnum.Viewer, RoleEnum.Editor, RoleEnum.Owner],
            )

    def get_openai_api_key(self, brain_id, user_id):
        brain_details = get_brain_details(brain_id)
        if brain_details:
            return brain_details.openai_api_key

    def get_answer_generator(
        self,
        brain_id,
        chat_id,
        model,
        max_tokens,
        temperature,
        user_openai_api_key,
        streaming,
        prompt_id,
    ):
        return QABaseBrainPicking(
            chat_id=chat_id,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            brain_id=brain_id,
            user_openai_api_key=user_openai_api_key,
            streaming=streaming,
            prompt_id=prompt_id,
        )
