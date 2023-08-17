import uuid
import pytest
from unittest.mock import patch, AsyncMock
from models.chats import ChatQuestion
from repository.chat.get_chat_history import GetChatHistoryOutput
from llm import HeadlessQA


@pytest.fixture
def mocked_openai_client():
    with patch('langchain.chat_models.ChatOpenAI') as MockChatOpenAI:
        mock_instance = MockChatOpenAI.return_value
        mock_instance.acall.return_value = AsyncMock()
        yield mock_instance


@pytest.fixture
def mocked_get_chat_history():
    with patch('repository.chat.get_chat_history.get_chat_history') as get_chat_history:
        get_chat_history.return_value = []  # Mocked chat history
        yield get_chat_history


# Similar fixtures for other dependencies
@pytest.mark.asyncio
async def test_generate_answer(mocked_openai_client, mocked_get_chat_history):
    headless_qa = HeadlessQA(model='gpt-3.5-turbo', openai_api_key='fake_api_key')

    question = ChatQuestion(question="What's your favorite color?", brain_id=None)
    chat_id = uuid.uuid4()

    result = headless_qa.generate_answer(chat_id, question)

    assert isinstance(result, GetChatHistoryOutput)
    assert result.user_message == question.question

    mocked_get_chat_history.assert_called_once_with(chat_id)
    mocked_openai_client.assert_called_once()
    assert mocked_openai_client.return_value.acall.called


@pytest.mark.asyncio
async def test_generate_stream(mocked_openai_client, mocked_get_chat_history):
    headless_qa = HeadlessQA(model='gpt-3.5-turbo', openai_api_key='fake_api_key')

    question = ChatQuestion(question="What's your favorite color?", brain_id=None)
    chat_id = uuid.uuid4()

    async for item in headless_qa.generate_stream(chat_id, question):
        assert "data: " in item

    mocked_get_chat_history.assert_called_once_with(chat_id)
    mocked_openai_client.assert_called_once()
    assert mocked_openai_client.return_value.acall.called

# More test cases for different scenarios and edge cases
