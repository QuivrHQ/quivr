import unittest
from unittest.mock import patch
import uuid
from repository.chat.get_chat_history import GetChatHistoryOutput
import repository.chat.get_chat_history
from llm import HeadlessQA
from models.chats import ChatQuestion  # Import the ChatQuestion class or provide a mock


def mock_get_chat_history(chat_id):
    history = GetChatHistoryOutput(
        chat_id=uuid.uuid4(),
        message_id=uuid.uuid4(),
        user_message="Test message",
        assistant="Test assistant",
        message_time="Test time",
        prompt_title="Test title",
        brain_name=None,)
    return [history]


class TestHeadlessQA(unittest.TestCase):
    def test_generate_answer(self):
        # Create a mock ChatQuestion instance
        question = ChatQuestion(question="Test question", brain_id=None)
        # Create an instance of HeadlessQA (replace the arguments with your actual values)
        headless_qa = HeadlessQA(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=256,
            openai_api_key="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",
        )
        # Call the generate_answer method
        chat_id = uuid.uuid4()
        with patch("qa_headless.get_chat_history", mock_get_chat_history):
            result = headless_qa.generate_answer(chat_id=chat_id, question=question)
            # Perform assertions on the result
            assert isinstance(result, GetChatHistoryOutput)
