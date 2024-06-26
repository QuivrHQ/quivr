import logging
from typing import Any, Dict, List, Tuple

from langchain.schema import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    format_document,
)
from langchain_core.messages.ai import AIMessageChunk

from quivr_core.models import (
    GetChatHistoryOutput,
    ParsedRAGChunkResponse,
    ParsedRAGResponse,
    QuivrKnowledge,
    RAGResponseMetadata,
    RawRAGResponse,
)
from quivr_core.prompts import DEFAULT_DOCUMENT_PROMPT

# TODO(@aminediro): define a types packages where we clearly define IO types
# This should be used for serialization/deseriallization later


logger = logging.getLogger(__name__)


def model_supports_function_calling(model_name: str):
    models_supporting_function_calls = [
        "gpt-4",
        "gpt-4-1106-preview",
        "gpt-4-0613",
        "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo-0613",
        "gpt-4-0125-preview",
        "gpt-3.5-turbo",
        "gpt-4-turbo",
        "gpt-4o",
    ]
    return model_name in models_supporting_function_calls


def format_chat_history(
    history: List[GetChatHistoryOutput],
) -> List[Dict[str, str]]:
    """Format the chat history into a list of HumanMessage and AIMessage"""
    formatted_history = []
    for chat in history:
        if chat.user_message:
            formatted_history.append(HumanMessage(content=chat.user_message))
        if chat.assistant:
            formatted_history.append(AIMessage(content=chat.assistant))
    return formatted_history


def format_history_to_openai_mesages(
    tuple_history: List[Tuple[str, str]], system_message: str, question: str
) -> List[BaseMessage]:
    """Format the chat history into a list of Base Messages"""
    messages = []
    messages.append(SystemMessage(content=system_message))
    for human, ai in tuple_history:
        messages.append(HumanMessage(content=human))
        messages.append(AIMessage(content=ai))
    messages.append(HumanMessage(content=question))
    return messages


def cited_answer_filter(tool):
    return tool["name"] == "cited_answer"


def get_prev_message_str(msg: AIMessageChunk) -> str:
    if msg.tool_calls:
        cited_answer = next(x for x in msg.tool_calls if cited_answer_filter(x))
        if "args" in cited_answer and "answer" in cited_answer["args"]:
            return cited_answer["args"]["answer"]
    return ""


def get_chunk_metadata(
    msg: AIMessageChunk, sources: list[Any] = []
) -> RAGResponseMetadata:
    # Initiate the source
    metadata = {"sources": sources}
    if msg.tool_calls:
        cited_answer = next(x for x in msg.tool_calls if cited_answer_filter(x))

        if "args" in cited_answer:
            gathered_args = cited_answer["args"]
            if "citations" in gathered_args:
                citations = gathered_args["citations"]
                metadata["citations"] = citations

            if "followup_questions" in gathered_args:
                followup_questions = gathered_args["followup_questions"]
                metadata["followup_questions"] = followup_questions

            if "thoughts" in gathered_args:
                thoughts = gathered_args["thoughts"]
                metadata["thoughts"] = thoughts

    return RAGResponseMetadata(**metadata)


# TODO: CONVOLUTED LOGIC !
# TODO(@aminediro): redo this
def parse_chunk_response(
    gathered_msg: AIMessageChunk,
    raw_chunk: dict[str, Any],
    supports_func_calling: bool,
) -> Tuple[AIMessageChunk, ParsedRAGChunkResponse]:
    # Init with sources
    answer_str = ""
    # Get the previously parsed answer
    prev_answer = get_prev_message_str(gathered_msg)

    if supports_func_calling:
        gathered_msg += raw_chunk["answer"]
        if gathered_msg.tool_calls:
            cited_answer = next(
                x for x in gathered_msg.tool_calls if cited_answer_filter(x)
            )
            if "args" in cited_answer:
                gathered_args = cited_answer["args"]
                if "answer" in gathered_args:
                    # Only send the difference between answer and response_tokens which was the previous answer
                    gathered_answer = gathered_args["answer"]
                    answer_str: str = gathered_answer[len(prev_answer) :]

        return gathered_msg, ParsedRAGChunkResponse(
            answer=answer_str, metadata=RAGResponseMetadata()
        )
    else:
        return gathered_msg, ParsedRAGChunkResponse(
            answer=raw_chunk["answer"].content, metadata=RAGResponseMetadata()
        )


def parse_response(raw_response: RawRAGResponse, model_name: str) -> ParsedRAGResponse:
    answer = raw_response["answer"].content
    sources = raw_response["docs"] or []

    metadata = {"sources": sources}

    if model_supports_function_calling(model_name):
        if raw_response["answer"].tool_calls:
            citations = raw_response["answer"].tool_calls[-1]["args"]["citations"]
            metadata["citations"] = citations
            followup_questions = raw_response["answer"].tool_calls[-1]["args"][
                "followup_questions"
            ]
            thoughts = raw_response["answer"].tool_calls[-1]["args"]["thoughts"]
            if followup_questions:
                metadata["followup_questions"] = followup_questions
            if thoughts:
                metadata["thoughts"] = thoughts
            answer = raw_response["answer"].tool_calls[-1]["args"]["answer"]

    parsed_response = ParsedRAGResponse(
        answer=answer, metadata=RAGResponseMetadata(**metadata)
    )
    return parsed_response


def combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    # for each docs, add an index in the metadata to be able to cite the sources
    for doc, index in zip(docs, range(len(docs))):
        doc.metadata["index"] = index
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def format_file_list(
    list_files_array: list[QuivrKnowledge], max_files: int = 20
) -> str:
    list_files = [file.file_name or file.url for file in list_files_array]
    files: list[str] = list(filter(lambda n: n is not None, list_files))  # type: ignore
    files = files[:max_files]

    files_str = "\n".join(files) if list_files_array else "None"
    return files_str
