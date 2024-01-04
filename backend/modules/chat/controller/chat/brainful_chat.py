from fastapi import HTTPException
from llm.api_brain_qa import APIBrainQA
from llm.composite_brain_qa import CompositeBrainQA
from llm.knowledge_brain_qa import KnowledgeBrainQA
from modules.brain.entity.brain_entity import BrainType, RoleEnum
from modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from modules.brain.service.brain_service import BrainService
from modules.chat.controller.chat.interface import ChatInterface

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
        brain_id,
        chat_id,
        model,
        max_tokens,
        temperature,
        streaming,
        prompt_id,
        user_id,
    ):
        brain = brain_service.get_brain_by_id(brain_id)

        if not brain:
            raise HTTPException(status_code=404, detail="Brain not found")

        if (
            brain.brain_type == BrainType.DOC
            or model not in models_supporting_function_calls
        ):
            return KnowledgeBrainQA(
                chat_id=chat_id,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                brain_id=brain_id,
                streaming=streaming,
                prompt_id=prompt_id,
            )
        if brain.brain_type == BrainType.COMPOSITE:
            return CompositeBrainQA(
                chat_id=chat_id,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                brain_id=brain_id,
                streaming=streaming,
                prompt_id=prompt_id,
                user_id=user_id,
            )

        return APIBrainQA(
            chat_id=chat_id,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            brain_id=brain_id,
            streaming=streaming,
            prompt_id=prompt_id,
            user_id=user_id,
        )
