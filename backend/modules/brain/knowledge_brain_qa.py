import asyncio
import json
from typing import AsyncIterable, Awaitable, List, Optional
from uuid import UUID

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from llm.utils.format_chat_history import format_chat_history
from llm.utils.get_prompt_to_use import get_prompt_to_use
from llm.utils.get_prompt_to_use_id import get_prompt_to_use_id
from logger import get_logger
from models import BrainSettings
from modules.brain.qa_interface import QAInterface
from modules.brain.rags.quivr_rag import QuivrRAG
from modules.brain.rags.rag_interface import RAGInterface
from modules.brain.service.brain_service import BrainService
from modules.chat.dto.chats import ChatQuestion, Sources
from modules.chat.dto.inputs import CreateChatHistory
from modules.chat.dto.outputs import GetChatHistoryOutput
from modules.chat.service.chat_service import ChatService
from pydantic import BaseModel
from repository.files.generate_file_signed_url import generate_file_signed_url

logger = get_logger(__name__)
QUIVR_DEFAULT_PROMPT = "Your name is Quivr. You're a helpful assistant.  If you don't know the answer, just say that you don't know, don't try to make up an answer."


brain_service = BrainService()
chat_service = ChatService()


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def generate_source(result, brain):
    # Initialize an empty list for sources
    sources_list: List[Sources] = []

    # Initialize a dictionary for storing generated URLs
    generated_urls = {}

    # Get source documents from the result, default to an empty list if not found
    source_documents = result.get("source_documents", [])

    # If source documents exist
    if source_documents:
        logger.info(f"Source documents found: {source_documents}")
        # Iterate over each document
        for doc in source_documents:
            # Check if 'url' is in the document metadata
            logger.info(f"Metadata 1: {doc.metadata}")
            is_url = (
                "original_file_name" in doc.metadata
                and doc.metadata["original_file_name"] is not None
                and doc.metadata["original_file_name"].startswith("http")
            )
            logger.info(f"Is URL: {is_url}")

            # Determine the name based on whether it's a URL or a file
            name = (
                doc.metadata["original_file_name"]
                if is_url
                else doc.metadata["file_name"]
            )

            # Determine the type based on whether it's a URL or a file
            type_ = "url" if is_url else "file"

            # Determine the source URL based on whether it's a URL or a file
            if is_url:
                source_url = doc.metadata["original_file_name"]
            else:
                file_path = f"{brain.brain_id}/{doc.metadata['file_name']}"
                # Check if the URL has already been generated
                if file_path in generated_urls:
                    source_url = generated_urls[file_path]
                else:
                    source_url = generate_file_signed_url(file_path).get(
                        "signedURL", ""
                    )
                    # Store the generated URL
                    generated_urls[file_path] = source_url

            # Append a new Sources object to the list
            sources_list.append(
                Sources(
                    name=name,
                    type=type_,
                    source_url=source_url,
                    original_file_name=name,
                )
            )
    else:
        logger.info("No source documents found or source_documents is not a list.")
    return sources_list


class KnowledgeBrainQA(BaseModel, QAInterface):
    """
    Main class for the Brain Picking functionality.
    It allows to initialize a Chat model, generate questions and retrieve answers using ConversationalRetrievalChain.
    It has two main methods: `generate_question` and `generate_stream`.
    One is for generating questions in a single request, the other is for generating questions in a streaming fashion.
    Both are the same, except that the streaming version streams the last message as a stream.
    Each have the same prompt template, which is defined in the `prompt_template` property.
    """

    class Config:
        """Configuration of the Pydantic Object"""

        arbitrary_types_allowed = True

    # Instantiate settings
    brain_settings = BrainSettings()  # type: ignore other parameters are optional

    # Default class attributes
    model: str = None  # pyright: ignore reportPrivateUsage=none
    temperature: float = 0.1
    chat_id: str = None  # pyright: ignore reportPrivateUsage=none
    brain_id: str  # pyright: ignore reportPrivateUsage=none
    max_tokens: int = 2000
    max_input: int = 2000
    streaming: bool = False
    knowledge_qa: Optional[RAGInterface]
    metadata: Optional[dict] = None

    callbacks: List[AsyncIteratorCallbackHandler] = (
        None  # pyright: ignore reportPrivateUsage=none
    )

    prompt_id: Optional[UUID]

    def __init__(
        self,
        model: str,
        brain_id: str,
        chat_id: str,
        max_tokens: int,
        streaming: bool = False,
        prompt_id: Optional[UUID] = None,
        metadata: Optional[dict] = None,
        **kwargs,
    ):
        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
            **kwargs,
        )
        self.prompt_id = prompt_id
        self.knowledge_qa = QuivrRAG(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
            **kwargs,
        )
        self.metadata = metadata
        self.max_tokens = max_tokens

    @property
    def prompt_to_use(self):
        if self.brain_id and is_valid_uuid(self.brain_id):
            return get_prompt_to_use(UUID(self.brain_id), self.prompt_id)
        else:
            return None

    @property
    def prompt_to_use_id(self) -> Optional[UUID]:
        # TODO: move to prompt service or instruction or something
        if self.brain_id and is_valid_uuid(self.brain_id):
            return get_prompt_to_use_id(UUID(self.brain_id), self.prompt_id)
        else:
            return None

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> GetChatHistoryOutput:
        transformed_history = format_chat_history(
            chat_service.get_chat_history(self.chat_id)
        )

        # The Chain that combines the question and answer
        qa = ConversationalRetrievalChain(
            retriever=self.knowledge_qa.get_retriever(),
            combine_docs_chain=self.knowledge_qa.get_doc_chain(
                streaming=False,
            ),
            question_generator=self.knowledge_qa.get_question_generation_llm(),
            verbose=False,
            rephrase_question=False,
            return_source_documents=True,
        )

        prompt_content = (
            self.prompt_to_use.content if self.prompt_to_use else QUIVR_DEFAULT_PROMPT
        )

        model_response = qa(
            {
                "question": question.question,
                "chat_history": transformed_history,
                "custom_personality": prompt_content,
            }
        )

        answer = model_response["answer"]

        brain = brain_service.get_brain_by_id(self.brain_id)

        if save_answer:
            # save the answer to the database or not ->  add a variable
            new_chat = chat_service.update_chat_history(
                CreateChatHistory(
                    **{
                        "chat_id": chat_id,
                        "user_message": question.question,
                        "assistant": answer,
                        "brain_id": brain.brain_id,
                        "prompt_id": self.prompt_to_use_id,
                    }
                )
            )

            return GetChatHistoryOutput(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": answer,
                    "message_time": new_chat.message_time,
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": brain.name if brain else None,
                    "message_id": new_chat.message_id,
                    "brain_id": str(brain.brain_id) if brain else None,
                }
            )

        return GetChatHistoryOutput(
            **{
                "chat_id": chat_id,
                "user_message": question.question,
                "assistant": answer,
                "message_time": None,
                "prompt_title": (
                    self.prompt_to_use.title if self.prompt_to_use else None
                ),
                "brain_name": None,
                "message_id": None,
                "brain_id": str(brain.brain_id) if brain else None,
            }
        )

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        history = chat_service.get_chat_history(self.chat_id)
        callback = AsyncIteratorCallbackHandler()
        self.callbacks = [callback]

        # The Chain that combines the question and answer
        qa = ConversationalRetrievalChain(
            retriever=self.knowledge_qa.get_retriever(),
            combine_docs_chain=self.knowledge_qa.get_doc_chain(
                callbacks=self.callbacks,
                streaming=True,
            ),
            question_generator=self.knowledge_qa.get_question_generation_llm(),
            verbose=False,
            rephrase_question=False,
            return_source_documents=True,
        )

        transformed_history = format_chat_history(history)

        response_tokens = []

        async def wrap_done(fn: Awaitable, event: asyncio.Event):
            try:
                return await fn
            except Exception as e:
                logger.error(f"Caught exception: {e}")
                return None  # Or some sentinel value that indicates failure
            finally:
                event.set()

        prompt_content = self.prompt_to_use.content if self.prompt_to_use else None
        run = asyncio.create_task(
            wrap_done(
                qa.acall(
                    {
                        "question": question.question,
                        "chat_history": transformed_history,
                        "custom_personality": prompt_content,
                    }
                ),
                callback.done,
            )
        )

        brain = brain_service.get_brain_by_id(self.brain_id)

        if save_answer:
            streamed_chat_history = chat_service.update_chat_history(
                CreateChatHistory(
                    **{
                        "chat_id": chat_id,
                        "user_message": question.question,
                        "assistant": "",
                        "brain_id": brain.brain_id,
                        "prompt_id": self.prompt_to_use_id,
                    }
                )
            )

            streamed_chat_history = GetChatHistoryOutput(
                **{
                    "chat_id": str(chat_id),
                    "message_id": streamed_chat_history.message_id,
                    "message_time": streamed_chat_history.message_time,
                    "user_message": question.question,
                    "assistant": "",
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": brain.name if brain else None,
                    "brain_id": str(brain.brain_id) if brain else None,
                    "metadata": self.metadata,
                }
            )
        else:
            streamed_chat_history = GetChatHistoryOutput(
                **{
                    "chat_id": str(chat_id),
                    "message_id": None,
                    "message_time": None,
                    "user_message": question.question,
                    "assistant": "",
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": brain.name if brain else None,
                    "brain_id": str(brain.brain_id) if brain else None,
                    "metadata": self.metadata,
                }
            )

        try:
            async for token in callback.aiter():
                logger.debug("Token: %s", token)
                response_tokens.append(token)
                streamed_chat_history.assistant = token
                yield f"data: {json.dumps(streamed_chat_history.dict())}"
        except Exception as e:
            logger.error("Error during streaming tokens: %s", e)
        try:
            # Python

            # Await the run
            result = await run

            sources_list = generate_source(result, brain)
            # Create metadata if it doesn't exist
            if not streamed_chat_history.metadata:
                streamed_chat_history.metadata = {}
                # Serialize the sources list
            serialized_sources_list = [source.dict() for source in sources_list]
            streamed_chat_history.metadata["sources"] = serialized_sources_list
            yield f"data: {json.dumps(streamed_chat_history.dict())}"

        except Exception as e:
            logger.error("Error processing source documents: %s", e)

        # Combine all response tokens to form the final assistant message
        assistant = "".join(response_tokens)

        try:
            if save_answer:
                chat_service.update_message_by_id(
                    message_id=str(streamed_chat_history.message_id),
                    user_message=question.question,
                    assistant=assistant,
                    metadata=streamed_chat_history.metadata,
                )
        except Exception as e:
            logger.error("Error updating message by ID: %s", e)
