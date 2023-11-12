from fastapi import HTTPException
from llm.api_brain_qa import APIBrainQA
from llm.qa_base import QABaseBrainPicking
from models.brain_entity import BrainType
from repository.brain import get_brain_details
from repository.brain.get_brain_by_id import get_brain_by_id
from routes.authorizations.brain_authorization import validate_brain_authorization
from routes.authorizations.types import RoleEnum
from routes.chat.interface import ChatInterface

models_supporting_function_calls = [
    "gpt-4",
    "gpt-4-1106-preview",
    "gpt-4-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0613",
]


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
        user_id,
    ):
        brain = get_brain_by_id(brain_id)

        if not brain:
            raise HTTPException(status_code=404, detail="Brain not found")

        if (
            brain.brain_type == BrainType.DOC
            or model not in models_supporting_function_calls
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

        return APIBrainQA(
            chat_id=chat_id,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            brain_id=brain_id,
            user_openai_api_key=user_openai_api_key,
            streaming=streaming,
            prompt_id=prompt_id,
            user_id=user_id,
        )
