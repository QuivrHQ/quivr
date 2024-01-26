from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from llm.api_brain_qa import APIBrainQA
from llm.composite_brain_qa import CompositeBrainQA
from llm.knowledge_brain_qa import KnowledgeBrainQA
from logger import get_logger
from models.settings import BrainSettings, get_supabase_client
from modules.brain.entity.brain_entity import BrainType, RoleEnum
from modules.brain.service.api_brain_definition_service import ApiBrainDefinitionService
from modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from modules.brain.service.brain_service import BrainService
from modules.chat.controller.chat.interface import ChatInterface
from modules.chat.service.chat_service import ChatService
from vectorstore.supabase import CustomSupabaseVectorStore

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
        brain_id,
        chat_id,
        model,
        max_tokens,
        temperature,
        streaming,
        prompt_id,
        user_id,
        chat_question,
    ):
        metadata = {}
        brain_settings = BrainSettings()
        supabase_client = get_supabase_client()
        embeddings = None
        if brain_settings.ollama_api_base_url:
            embeddings = OllamaEmbeddings(
                base_url=brain_settings.ollama_api_base_url
            )  # pyright: ignore reportPrivateUsage=none
        else:
            embeddings = OpenAIEmbeddings()
        vector_store = CustomSupabaseVectorStore(
            supabase_client, embeddings, table_name="vectors", user_id=user_id
        )

        # Init

        brain_id_to_use = brain_id

        # Get the first question from the chat_question

        question = chat_question.question
        history = chat_service.get_chat_history(chat_id)

        list_brains = []  # To return

        if history and not brain_id_to_use:
            # Replace the question with the first question from the history
            question = history[0].user_message

        if history and not brain_id:
            brain_id_to_use = history[0].brain_id

        # Calculate the closest brains to the question
        list_brains = vector_store.find_brain_closest_query(user_id, question)

        metadata["close_brains"] = list_brains[:5]

        if list_brains and not brain_id_to_use:
            brain_id_to_use = list_brains[0]["id"]

        # GENERIC
        follow_up_questions = chat_service.get_follow_up_question(chat_id)
        metadata["follow_up_questions"] = follow_up_questions
        metadata["model"] = model
        metadata["max_tokens"] = max_tokens
        metadata["temperature"] = temperature

        brain = brain_service.get_brain_by_id(brain_id_to_use)
        if (
            brain
            and brain.brain_type == BrainType.DOC
            or model not in models_supporting_function_calls
        ):
            return KnowledgeBrainQA(
                chat_id=chat_id,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                brain_id=str(brain.brain_id),
                streaming=streaming,
                prompt_id=prompt_id,
                metadata=metadata,
            )
        if brain.brain_type == BrainType.COMPOSITE:
            return CompositeBrainQA(
                chat_id=chat_id,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                brain_id=str(brain.brain_id),
                streaming=streaming,
                prompt_id=prompt_id,
                user_id=user_id,
                metadata=metadata,
            )

        if brain.brain_type == BrainType.API:
            brain_definition = api_brain_definition_service.get_api_brain_definition(
                brain_id_to_use
            )
            return APIBrainQA(
                chat_id=chat_id,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                brain_id=str(brain.brain_id),
                streaming=streaming,
                prompt_id=prompt_id,
                user_id=user_id,
                metadata=metadata,
                raw=brain_definition.raw,
                jq_instructions=brain_definition.jq_instructions,
            )
