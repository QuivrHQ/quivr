from time import sleep
from uuid import uuid4

import pytest
from langchain_core.messages import AIMessage, HumanMessage
from quivr_core.rag.entities.chat import ChatHistory


@pytest.fixture
def ai_message():
    return AIMessage("ai message")


@pytest.fixture
def human_message():
    return HumanMessage("human message")


def test_chat_history_constructor():
    brain_id, chat_id = uuid4(), uuid4()
    chat_history = ChatHistory(brain_id=brain_id, chat_id=chat_id)

    assert chat_history.brain_id == brain_id
    assert chat_history.id == chat_id
    assert len(chat_history._msgs) == 0


def test_chat_history_append(ai_message: AIMessage, human_message: HumanMessage):
    chat_history = ChatHistory(uuid4(), uuid4())
    chat_history.append(ai_message)

    assert len(chat_history) == 1
    chat_history.append(human_message)
    assert len(chat_history) == 2


def test_chat_history_get_history(ai_message: AIMessage, human_message: HumanMessage):
    chat_history = ChatHistory(uuid4(), uuid4())
    chat_history.append(ai_message)
    chat_history.append(human_message)
    chat_history.append(ai_message)
    sleep(0.01)
    chat_history.append(human_message)

    msgs = chat_history.get_chat_history()

    assert len(msgs) == 4
    assert msgs[-1].message_time > msgs[0].message_time
    assert isinstance(msgs[0].msg, AIMessage)
    assert isinstance(msgs[1].msg, HumanMessage)

    msgs = chat_history.get_chat_history(newest_first=True)
    assert msgs[-1].message_time < msgs[0].message_time


def test_chat_history_iter_pairs_invalid(
    ai_message: AIMessage, human_message: HumanMessage
):
    with pytest.raises(AssertionError):
        chat_history = ChatHistory(uuid4(), uuid4())
        chat_history.append(ai_message)
        chat_history.append(ai_message)
        next(chat_history.iter_pairs())


def test_chat_history_iter_pais(ai_message: AIMessage, human_message: HumanMessage):
    chat_history = ChatHistory(uuid4(), uuid4())

    chat_history.append(human_message)
    chat_history.append(ai_message)
    chat_history.append(human_message)
    chat_history.append(ai_message)

    result = list(chat_history.iter_pairs())

    assert result == [(human_message, ai_message), (human_message, ai_message)]
