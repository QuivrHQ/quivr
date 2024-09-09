from uuid import uuid4

import pytest
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.messages.tool import ToolCall

from quivr_core.utils import (
    get_prev_message_str,
    model_supports_function_calling,
    parse_chunk_response,
)


def test_model_supports_function_calling():
    assert model_supports_function_calling("gpt-4") is True
    assert model_supports_function_calling("ollama3") is False


def test_get_prev_message_incorrect_message():
    with pytest.raises(StopIteration):
        chunk = AIMessageChunk(
            content="",
            tool_calls=[ToolCall(name="test", args={"answer": ""}, id=str(uuid4()))],
        )
        assert get_prev_message_str(chunk) == ""


def test_get_prev_message_str():
    chunk = AIMessageChunk(content="")
    assert get_prev_message_str(chunk) == ""
    # Test a correct chunk
    chunk = AIMessageChunk(
        content="",
        tool_calls=[
            ToolCall(
                name="cited_answer",
                args={"answer": "this is an answer"},
                id=str(uuid4()),
            )
        ],
    )
    assert get_prev_message_str(chunk) == "this is an answer"


def test_parse_chunk_response_nofunc_calling():
    rolling_msg = AIMessageChunk(content="")
    chunk = {
        "answer": AIMessageChunk(
            content="next ",
        )
    }
    for i in range(10):
        rolling_msg, parsed_chunk = parse_chunk_response(rolling_msg, chunk, False)
        assert rolling_msg.content == "next " * (i + 1)
        assert parsed_chunk == "next "


def _check_rolling_msg(rol_msg: AIMessageChunk) -> bool:
    return (
        len(rol_msg.tool_calls) > 0
        and rol_msg.tool_calls[0]["name"] == "cited_answer"
        and rol_msg.tool_calls[0]["args"] is not None
        and "answer" in rol_msg.tool_calls[0]["args"]
    )


def test_parse_chunk_response_func_calling(chunks_stream_answer):
    rolling_msg = AIMessageChunk(content="")

    rolling_msgs_history = []
    answer_str_history: list[str] = []

    for chunk in chunks_stream_answer:
        # This is done
        rolling_msg, answer_str = parse_chunk_response(rolling_msg, chunk, True)
        rolling_msgs_history.append(rolling_msg)
        answer_str_history.append(answer_str)

    # Checks that we accumulate into correctly
    last_rol_msg = None
    last_answer_chunk = None

    # TEST1:
    # Asserting that parsing accumulates the chunks
    for rol_msg in rolling_msgs_history:
        if last_rol_msg is not None:
            # Check tool_call_chunks accumulated correctly
            assert (
                len(rol_msg.tool_call_chunks) > 0
                and rol_msg.tool_call_chunks[0]["name"] == "cited_answer"
                and rol_msg.tool_call_chunks[0]["args"]
            )
            answer_chunk = rol_msg.tool_call_chunks[0]["args"]
            # assert that the answer is accumulated
            assert last_answer_chunk in answer_chunk

        if _check_rolling_msg(rol_msg):
            last_rol_msg = rol_msg
            last_answer_chunk = rol_msg.tool_call_chunks[0]["args"]

    # TEST2:
    # Progressively acc answer string
    assert all(
        answer_str_history[i] in answer_str_history[i + 1]
        for i in range(len(answer_str_history) - 1)
    )
    # NOTE: Last chunk's answer should match the accumulated history
    assert last_rol_msg.tool_calls[0]["args"]["answer"] == answer_str_history[-1]  # type: ignore
