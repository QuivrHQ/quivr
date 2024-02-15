import json
from typing import AsyncIterable
from uuid import UUID

from langchain_community.chat_models import ChatLiteLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from modules.chat.dto.chats import ChatQuestion


class GPT4Brain(KnowledgeBrainQA):
    """This is the Notion brain class. it is a KnowledgeBrainQA has the data is stored locally.
    It is going to call the Data Store internally to get the data.

    Args:
        KnowledgeBrainQA (_type_): A brain that store the knowledge internaly
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

    def get_chain(self):

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are GPT-4 powered by Quivr. You are an assistant."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        chain = prompt | ChatLiteLLM(
            model="gpt-4-0125-preview", max_tokens=self.max_tokens
        )

        return chain

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        conversational_qa_chain = self.get_chain()
        transformed_history, streamed_chat_history = (
            self.initialize_streamed_chat_history(chat_id, question)
        )
        response_tokens = []

        async for chunk in conversational_qa_chain.astream(
            {
                "question": question.question,
                "chat_history": transformed_history,
            }
        ):
            response_tokens.append(chunk.content)
            streamed_chat_history.assistant = chunk.content
            yield f"data: {json.dumps(streamed_chat_history.dict())}"

        self.save_answer(question, response_tokens, streamed_chat_history, save_answer)
