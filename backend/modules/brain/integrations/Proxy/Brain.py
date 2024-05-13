import json
from typing import AsyncIterable
from uuid import UUID

from langchain_community.chat_models import ChatLiteLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from logger import get_logger
from modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from modules.chat.dto.chats import ChatQuestion
from modules.chat.dto.outputs import GetChatHistoryOutput
from modules.chat.service.chat_service import ChatService

logger = get_logger(__name__)

chat_service = ChatService()


class ProxyBrain(KnowledgeBrainQA):
    """
    ProxyBrain class serves as a proxy to utilize various language models for generating responses.
    It dynamically selects and uses the appropriate language model based on the provided context and question.
    """

    def __init__(
        self,
        **kwargs,
    ):
        """
        Initializes the ProxyBrain with the given arguments.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(
            **kwargs,
        )

    def get_chain(self):
        """
        Constructs and returns the conversational chain for ProxyBrain.

        Returns:
            A conversational chain object.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are Quivr. You are an assistant. {custom_personality}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        chain = prompt | ChatLiteLLM(model=self.model, max_tokens=self.max_tokens)

        return chain

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        """
        Generates a stream of responses for the given question.

        Args:
            chat_id (UUID): The chat session ID.
            question (ChatQuestion): The question object.
            save_answer (bool): Whether to save the answer.

        Yields:
            AsyncIterable: A stream of response strings.
        """
        conversational_qa_chain = self.get_chain()
        transformed_history, streamed_chat_history = (
            self.initialize_streamed_chat_history(chat_id, question)
        )
        response_tokens = []
        config = {"metadata": {"conversation_id": str(chat_id)}}

        async for chunk in conversational_qa_chain.astream(
            {
                "question": question.question,
                "chat_history": transformed_history,
                "custom_personality": (
                    self.prompt_to_use.content if self.prompt_to_use else None
                ),
            },
            config=config,
        ):
            response_tokens.append(chunk.content)
            streamed_chat_history.assistant = chunk.content
            yield f"data: {json.dumps(streamed_chat_history.dict())}"

        self.save_answer(question, response_tokens, streamed_chat_history, save_answer)

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> GetChatHistoryOutput:
        """
        Generates a non-streaming answer for the given question.

        Args:
            chat_id (UUID): The chat session ID.
            question (ChatQuestion): The question object.
            save_answer (bool): Whether to save the answer.

        Returns:
            GetChatHistoryOutput: The chat history output object containing the answer.
        """
        conversational_qa_chain = self.get_chain()
        transformed_history, streamed_chat_history = (
            self.initialize_streamed_chat_history(chat_id, question)
        )
        config = {"metadata": {"conversation_id": str(chat_id)}}
        model_response = conversational_qa_chain.invoke(
            {
                "question": question.question,
                "chat_history": transformed_history,
                "custom_personality": (
                    self.prompt_to_use.content if self.prompt_to_use else None
                ),
            },
            config=config,
        )

        answer = model_response.content

        return self.save_non_streaming_answer(
            chat_id=chat_id,
            question=question,
            answer=answer,
        )
