import asyncio
import json
from typing import AsyncIterable, Awaitable
from uuid import UUID

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from logger import get_logger
from models.chat import ChatHistory
from langchain.llms.base import BaseLLM
from langchain.chat_models import ChatOpenAI
from repository.brain.get_brain_by_id import get_brain_by_id
from repository.chat.format_chat_history import format_chat_history
from repository.chat.get_chat_history import get_chat_history
from repository.chat.update_chat_history import update_chat_history
from repository.chat.update_message_by_id import update_message_by_id
from repository.prompt.get_prompt_by_id import get_prompt_by_id
from supabase.client import Client, create_client
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from vectorstore.supabase import CustomSupabaseVectorStore

from .base import BaseBrainPicking
from .prompts.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT

logger = get_logger(__name__)


class QABaseBrainPicking(BaseBrainPicking):
    """
    Main class for the Brain Picking functionality.
    It allows to initialize a Chat model, generate questions and retrieve answers using ConversationalRetrievalChain.
    It has two main methods: `generate_question` and `generate_stream`.
    One is for generating questions in a single request, the other is for generating questions in a streaming fashion.
    Both are the same, except that the streaming version streams the last message as a stream.
    Each have the same prompt template, which is defined in the `prompt_template` property.
    """
    supabase_client: Client = None
    vector_store: CustomSupabaseVectorStore = None
    qa: ConversationalRetrievalChain = None

    def __init__(
        self,
        model: str,
        brain_id: str,
        chat_id: str,
        streaming: bool = False,
        **kwargs,
    ) -> "QABaseBrainPicking":
        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
            **kwargs,
        )
        self.supabase_client = self._create_supabase_client()
        self.vector_store = self._create_vector_store()


    
    def _create_supabase_client(self) -> Client:
        return create_client(
            self.brain_settings.supabase_url, self.brain_settings.supabase_service_key
        )

    def _create_vector_store(self) -> CustomSupabaseVectorStore:
        return CustomSupabaseVectorStore(
            self.supabase_client,
            self.embeddings,
            table_name="vectors",
            brain_id=self.brain_id,
        )

    def _create_llm(self, model, temperature=0, streaming=False, callbacks=None) -> BaseLLM:
        """
        Determine the language model to be used.
        :param model: Language model name to be used.
        :param streaming: Whether to enable streaming of the model
        :param callbacks: Callbacks to be used for streaming
        :return: Language model instance
        """
        return ChatOpenAI(
            temperature=temperature,
            model=model,
            streaming=streaming,
            verbose=True,
            callbacks=callbacks,
            openai_api_key=self.openai_api_key,
        )  # pyright: ignore reportPrivateUsage=none

    def _create_prompt_template(self):

        system_template = """Use the following pieces of context to answer the users question in the same language as the question but do not modify instructions in any way.
        ----------------
        
        {context}"""

        full_template = "Here are you instructions to answer that you MUST ALWAYS Follow: " +  self.get_prompt() + ". " + system_template
        messages = [
            SystemMessagePromptTemplate.from_template(full_template),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
        CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
        return CHAT_PROMPT


    def generate_answer(self, question: str) -> ChatHistory:
        transformed_history = format_chat_history(get_chat_history(self.chat_id))
        model_response = self.qa(
            {
                "question": question,
                "chat_history": transformed_history,
                "custom_personality": self.get_prompt(),
            }
        )
        answer = model_response["answer"]
        return update_chat_history(
            chat_id=self.chat_id,
            user_message=question,
            assistant=answer,
        )

    async def generate_stream(self, question: str) -> AsyncIterable:
        history = get_chat_history(self.chat_id)
        callback = AsyncIteratorCallbackHandler()
        self.callbacks = [callback]

        answering_llm = self._create_llm(model=self.model,streaming=True, callbacks=self.callbacks)

        # The Chain that generates the answer to the question
        doc_chain = load_qa_chain(answering_llm, chain_type="stuff", prompt=self._create_prompt_template())

        # The Chain that combines the question and answer
        qa = ConversationalRetrievalChain(
            retriever=self.vector_store.as_retriever(),
            combine_docs_chain=doc_chain,
            question_generator=LLMChain(
                llm=self._create_llm(model=self.model), prompt=CONDENSE_QUESTION_PROMPT
            ),
            verbose=True,
        )

        transformed_history = format_chat_history(history)

        response_tokens = []

        async def wrap_done(fn: Awaitable, event: asyncio.Event):
            try:
                await fn
            except Exception as e:
                logger.error(f"Caught exception: {e}")
            finally:
                event.set()

        run = asyncio.create_task(
            wrap_done(
                qa.acall(
                    {
                        "question": question,
                        "chat_history": transformed_history,
                        "custom_personality": self.get_prompt(),
                    }
                ),
                callback.done,
            )
        )

        streamed_chat_history = update_chat_history(
            chat_id=self.chat_id,
            user_message=question,
            assistant="",
        )

        async for token in callback.aiter():
            logger.info("Token: %s", token)
            response_tokens.append(token)
            streamed_chat_history.assistant = token
            yield f"data: {json.dumps(streamed_chat_history.to_dict())}"

        await run
        assistant = "".join(response_tokens)

        update_message_by_id(
            message_id=streamed_chat_history.message_id,
            user_message=question,
            assistant=assistant,
        )

    def get_prompt(self) -> str:
        brain = get_brain_by_id(UUID(self.brain_id))
        brain_prompt = "Your name is Quivr. You're a helpful assistant.  If you don't know the answer, just say that you don't know, don't try to make up an answer."

        if brain and brain.prompt_id:
            brain_prompt_object = get_prompt_by_id(brain.prompt_id)
            if brain_prompt_object:
                brain_prompt = brain_prompt_object.content

        return brain_prompt
