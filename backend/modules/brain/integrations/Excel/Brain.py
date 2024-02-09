import json
import os
from typing import AsyncIterable
from uuid import UUID

import pandas as pd
from llm.utils.format_chat_history import format_chat_history
from logger import get_logger
from modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from modules.brain.service.brain_service import BrainService
from modules.chat.dto.chats import ChatQuestion
from modules.chat.dto.inputs import CreateChatHistory
from modules.chat.dto.outputs import GetChatHistoryOutput
from modules.chat.service.chat_service import ChatService
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

logger = get_logger(__name__)

brain_service = BrainService()
chat_service = ChatService()


class ExcelBrain(KnowledgeBrainQA):
    """This is the Excel brain class. it is a KnowledgeBrainQA has the data is stored locally.
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

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        history = chat_service.get_chat_history(self.chat_id)
        brain = brain_service.get_brain_by_id(self.brain_id)
        transformed_history = format_chat_history(history)

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
        # Instantiate a LLM
        df = pd.read_csv("1500000_Sales_Records.csv")
        open_ai_api_key = os.environ.get("OPENAI_API_KEY")
        llm = OpenAI(api_token=open_ai_api_key)

        df = SmartDataframe(df, config={"llm": llm, "save_charts": True})
        answer = df.chat(question.question, output_type="string")
        streamed_chat_history.assistant = answer

        yield f"data: {json.dumps(streamed_chat_history.dict())}"
        logger.info("Streamed chat history")
        logger.info(answer)

        chat_service.update_message_by_id(
            message_id=str(streamed_chat_history.message_id),
            user_message=question.question,
            assistant=answer,
            metadata=streamed_chat_history.metadata,
        )
