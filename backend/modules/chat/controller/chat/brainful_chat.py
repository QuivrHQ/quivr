from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from llm.api_brain_qa import APIBrainQA
from llm.composite_brain_qa import CompositeBrainQA
from llm.knowledge_brain_qa import KnowledgeBrainQA
from logger import get_logger
from models.settings import BrainSettings, get_supabase_client
from modules.brain.entity.brain_entity import BrainType, RoleEnum
from modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from modules.brain.service.brain_service import BrainService
from modules.chat.controller.chat.interface import ChatInterface
from modules.chat.service.chat_service import ChatService
from vectorstore.supabase import CustomSupabaseVectorStore

chat_service = ChatService()

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
        brain_id_to_use = brain_id
        if not brain_id:
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
                supabase_client, embeddings, table_name="vectors"
            )
            # Get the first question from the chat_question
            logger.info(f"Finding brain closest to {chat_question}")
            logger.info("🔥🔥🔥🔥🔥")
            question = chat_question.question
            logger.info(f"Question is {question}")
            history = chat_service.get_chat_history(chat_id)
            if history:
                question = history[0].user_message
                logger.info(f"Question is {question}")
            brain_id_to_use = vector_store.find_brain_closest_query(question)
            logger.info(f"Found brain {brain_id_to_use}")
            logger.info("🧠🧠🧠")

        brain = brain_service.get_brain_by_id(brain_id_to_use)
        logger.info(f"Brain type: {brain.brain_type}")
        logger.info(f"Id is {brain.brain_id}")
        logger.info(f"Type of brain_id is {type(brain.brain_id)}")
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
            )

        if brain.brain_type == BrainType.API:
            return APIBrainQA(
                chat_id=chat_id,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                brain_id=str(brain.brain_id),
                streaming=streaming,
                prompt_id=prompt_id,
                user_id=user_id,
            )
