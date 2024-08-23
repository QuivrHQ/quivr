import logging
from operator import itemgetter
from typing import AsyncGenerator

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from quivr_core.chat import ChatHistory
from quivr_core.llm import LLMEndpoint
from quivr_core.models import (
    ChatLLMMetadata,
    ParsedRAGChunkResponse,
    ParsedRAGResponse,
    RAGResponseMetadata,
)
from quivr_core.utils import get_chunk_metadata, parse_response

logger = logging.getLogger("quivr_core")


class ChatLLM:
    def __init__(self, *, llm: LLMEndpoint):
        self.llm_endpoint = llm

    def filter_history(
        self,
        chat_history: ChatHistory | None,
    ):
        """
        Filter out the chat history to only include the messages that are relevant to the current question

        Returns a filtered chat_history with in priority: first max_tokens, then max_history where a Human message and an AI message count as one pair
        a token is 4 characters
        """
        total_tokens = 0
        total_pairs = 0
        filtered_chat_history: list[AIMessage | HumanMessage] = []
        if chat_history is None:
            return filtered_chat_history

        # Convert generator to list to allow reversing
        pairs = list(chat_history.iter_pairs())
        # Iterate in reverse to prioritize the last messages
        for human_message, ai_message in reversed(pairs):
            # TODO: replace with tiktoken
            message_tokens = (len(human_message.content) + len(ai_message.content)) // 4
            if (
                total_tokens + message_tokens > self.llm_endpoint._config.max_input
                or total_pairs >= 20
            ):
                break
            filtered_chat_history.append(human_message)
            filtered_chat_history.append(ai_message)
            total_tokens += message_tokens
            total_pairs += 1

        return filtered_chat_history[::-1]  # Reverse back to original order

    def build_chain(self):
        loaded_memory = RunnablePassthrough.assign(
            chat_history=RunnableLambda(
                lambda x: self.filter_history(x["chat_history"]),
            ),
            question=lambda x: x["question"],
        )
        logger.info(f"loaded_memory: {loaded_memory}")
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are Quivr. You are an assistant.",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        final_inputs = {
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
        }
        llm = self.llm_endpoint._llm

        answer = {"answer": final_inputs | prompt | llm, "docs": lambda _: []}

        return loaded_memory | answer

    def answer(
        self, question: str, history: ChatHistory | None = None
    ) -> ParsedRAGResponse:
        chain = self.build_chain()
        raw_llm_response = chain.invoke({"question": question, "chat_history": history})

        response = parse_response(raw_llm_response, self.llm_endpoint._config.model)
        return response

    async def answer_astream(
        self, question: str, history: ChatHistory | None = None
    ) -> AsyncGenerator[ParsedRAGChunkResponse, ParsedRAGChunkResponse]:
        chain = self.build_chain()
        rolling_message = AIMessageChunk(content="")
        prev_answer = ""
        chunk_id = 0

        async for chunk in chain.astream(
            {"question": question, "chat_history": history}
        ):
            if "answer" in chunk:
                answer_str = chunk["answer"].content
                rolling_message += chunk["answer"]
                if len(answer_str) > 0:
                    parsed_chunk = ParsedRAGChunkResponse(
                        answer=answer_str,
                        metadata=RAGResponseMetadata(),
                    )
                    prev_answer += answer_str

                    logger.debug(
                        f"answer_astream func_calling=True question={question} rolling_msg={rolling_message} chunk_id={chunk_id}, chunk={parsed_chunk}"
                    )
                    yield parsed_chunk

                    chunk_id += 1
        # Last chunk provides metadata
        last_chunk = ParsedRAGChunkResponse(
            answer=rolling_message.content,
            metadata=get_chunk_metadata(rolling_message),
            last_chunk=True,
        )
        last_chunk.metadata.metadata_model = ChatLLMMetadata(
            name=self.llm_endpoint._config.model,
        )
        logger.debug(
            f"answer_astream last_chunk={last_chunk} question={question} rolling_msg={rolling_message} chunk_id={chunk_id}"
        )
        yield last_chunk
