import json
from typing import AsyncIterable
from uuid import UUID

from langchain_community.chat_models import ChatLiteLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from quivr_api.modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from quivr_api.modules.chat.dto.chats import ChatQuestion


class ClaudeBrain(KnowledgeBrainQA):
    """
    ClaudeBrain integrates with Claude model to provide conversational AI capabilities.
    It leverages the Claude model for generating responses based on the provided context.

    Attributes:
        **kwargs: Arbitrary keyword arguments for KnowledgeBrainQA initialization.
    """

    def __init__(
        self,
        **kwargs,
    ):
        """
        Initializes the ClaudeBrain with the given arguments.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(
            **kwargs,
        )

    def calculate_pricing(self):
        """
        Calculates the pricing for using the ClaudeBrain.

        Returns:
            int: The pricing value.
        """
        return 3

    def get_chain(self):
        """
        Constructs and returns the conversational chain for ClaudeBrain.

        Returns:
            A conversational chain object.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are Claude powered by Quivr. You are an assistant. {custom_personality}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        chain = prompt | ChatLiteLLM(
            model="claude-3-haiku-20240307", max_tokens=self.max_tokens
        )

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

        async for chunk in conversational_qa_chain.astream(
            {
                "question": question.question,
                "chat_history": transformed_history,
                "custom_personality": (
                    self.prompt_to_use.content if self.prompt_to_use else None
                ),
            }
        ):
            response_tokens.append(chunk.content)
            streamed_chat_history.assistant = chunk.content
            yield f"data: {json.dumps(streamed_chat_history.dict())}"

        self.save_answer(question, response_tokens, streamed_chat_history, save_answer)
