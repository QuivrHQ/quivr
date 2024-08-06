import pytest

from quivr_core import ChatLLM


@pytest.mark.base
def test_chat_llm(fake_llm):
    chat_llm = ChatLLM(
        llm=fake_llm,
    )
    answer = chat_llm.answer("Hello, how are you?")

    assert len(answer.answer) > 0
    assert answer.metadata is not None
    assert answer.metadata.citations is None
    assert answer.metadata.followup_questions is None
    assert answer.metadata.sources == []
    assert answer.metadata.metadata_model is not None
    assert answer.metadata.metadata_model.name is not None
