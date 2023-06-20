import asyncio
import os
from typing import AsyncIterable, Awaitable
from uuid import UUID

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from llm.prompt.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT
from llm.prompt.LANGUAGE_PROMPT import QA_PROMPT
from llm.qa import create_clients_and_embeddings
from llm.vector_store import CustomSupabaseVectorStore
from logger import get_logger
from models.chats import ChatMessage
from models.users import User
from utils.common import CommonsDep
from utils.users import fetch_user_id_from_credentials

logger = get_logger(__name__)

stream_router = APIRouter()

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")


async def send_message(
    commons, chat_message: ChatMessage, current_user: User
) -> AsyncIterable[str]:
    user_id = fetch_user_id_from_credentials(commons, {"email": current_user.email})

    supabase_client, embeddings = create_clients_and_embeddings(
        openai_api_key, supabase_url, supabase_key
    )

    vector_store = CustomSupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors", user_id=user_id
    )

    callback = AsyncIteratorCallbackHandler()

    llm = ChatOpenAI(
        temperature=0,
        model_name=chat_message.model,
    )
    streaming_llm = ChatOpenAI(
        temperature=0,
        model_name=chat_message.model,
        streaming=True,
        callbacks=[callback],
    )

    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_chain(streaming_llm, chain_type="map_reduce")

    qa = ConversationalRetrievalChain(
        retriever=vector_store.as_retriever(),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
    )

    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
        try:
            resp = await fn
            logger.debug("Done: %s", resp)
        except Exception as e:
            # TODO: handle exception
            print(f"Caught exception: {e}")
        finally:
            # Signal the aiter to stop.
            event.set()

    # transformed_history = [(chat_message.history[i][1], chat_message.history[i + 1][1])
    #                        for i in range(0, len(chat_message.history) - 1, 2)]

    chat_history = []
    task = asyncio.create_task(
        wrap_done(
            await qa.a(
                {"question": chat_message.question, "chat_history": chat_history}
            ),
            callback.done,
        )
    )

    # task = asyncio.create_task(wrap_done(streaming_llm.agenerate(
    #     messages=[[HumanMessage(content=chat_message.question)]]), callback.done))

    async for token in callback.aiter():
        logger.info("Token: %s", token)
        # Use server-sent-events to stream the response
        yield f"data: {token}\n\n"

    await task


@stream_router.post("/stream", dependencies=[Depends(AuthBearer())], tags=["Stream"])
def stream(
    commons: CommonsDep,
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_user),
):
    return StreamingResponse(
        send_message(commons, chat_message, current_user),
        media_type="text/event-stream",
    )
