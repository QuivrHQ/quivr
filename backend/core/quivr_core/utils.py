import logging
from typing import Any, List, Tuple, no_type_check

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.prompts import format_document

from quivr_core.models import (
    ChatLLMMetadata,
    ParsedRAGResponse,
    QuivrKnowledge,
    RAGResponseMetadata,
    RawRAGResponse,
)
from quivr_core.prompts import custom_prompts

# TODO(@aminediro): define a types packages where we clearly define IO types
# This should be used for serialization/deseriallization later


logger = logging.getLogger("quivr_core")


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
        "gpt-4o-mini",
    ]
    return model_name in models_supporting_function_calls


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


def get_chunk_metadata(
    msg: AIMessageChunk, sources: list[Any] | None = None
) -> RAGResponseMetadata:
    # Initiate the source
    metadata = {"sources": sources} if sources else {"sources": []}
    all_citations = []
    all_followup_questions = []

    if msg.tool_calls:
        for cited_answer in filter(cited_answer_filter, msg.tool_calls):
            if "args" in cited_answer:
                gathered_args = cited_answer["args"]
                if "citations" in gathered_args:
                    all_citations.extend(gathered_args["citations"])
                if "followup_questions" in gathered_args:
                    all_followup_questions.append(gathered_args["followup_questions"])

    # Interleave follow-up questions
    interleaved_followup_questions = []
    max_length = (
        max(len(q) for q in all_followup_questions) if all_followup_questions else 0
    )
    for i in range(max_length):
        for questions in all_followup_questions:
            if i < len(questions):
                interleaved_followup_questions.append(questions[i])

    metadata["citations"] = all_citations
    metadata["followup_questions"] = interleaved_followup_questions[:3]  # Limit to 3

    return RAGResponseMetadata(**metadata, metadata_model=None)


def get_prev_message_str(msg: AIMessageChunk) -> str:
    if msg.tool_calls:
        cited_answer = next(x for x in msg.tool_calls if cited_answer_filter(x))
        if "args" in cited_answer and "answer" in cited_answer["args"]:
            return cited_answer["args"]["answer"]
    return ""


# TODO: CONVOLUTED LOGIC !
# TODO(@aminediro): redo this
@no_type_check
def parse_chunk_response(
    rolling_msg: AIMessageChunk,
    raw_chunk: dict[str, Any],
    supports_func_calling: bool,
) -> Tuple[AIMessageChunk, str]:
    # Init with sources
    answers = []

    if "answer" in raw_chunk:
        answer = raw_chunk["answer"]
    else:
        answer = raw_chunk

    rolling_msg += answer
    if supports_func_calling and rolling_msg.tool_calls:
        for cited_answer in filter(cited_answer_filter, rolling_msg.tool_calls):
            if "args" in cited_answer and "answer" in cited_answer["args"]:
                gathered_args = cited_answer["args"]
                answers.append(gathered_args["answer"])

    answer_str = "\n\n".join(answers) if answers else answer.content
    return rolling_msg, answer_str


@no_type_check
def parse_response(raw_response: RawRAGResponse, model_name: str) -> ParsedRAGResponse:
    answers = []
    sources = raw_response["docs"] if "docs" in raw_response else []

    metadata = RAGResponseMetadata(
        sources=sources, metadata_model=ChatLLMMetadata(name=model_name)
    )

    if (
        model_supports_function_calling(model_name)
        and "tool_calls" in raw_response["answer"]
        and raw_response["answer"].tool_calls
    ):
        all_citations = []
        all_followup_questions = []
        for tool_call in raw_response["answer"].tool_calls:
            if "args" in tool_call:
                args = tool_call["args"]
                if "citations" in args:
                    all_citations.extend(args["citations"])
                if "followup_questions" in args:
                    all_followup_questions.extend(args["followup_questions"])
                if "answer" in args:
                    answers.append(args["answer"])
        metadata.citations = all_citations
        metadata.followup_questions = all_followup_questions
    else:
        answers.append(raw_response["answer"].content)

    answer_str = "\n".join(answers)
    parsed_response = ParsedRAGResponse(answer=answer_str, metadata=metadata)
    return parsed_response


def combine_documents(
    docs,
    document_prompt=custom_prompts.DEFAULT_DOCUMENT_PROMPT,
    document_separator="\n\n",
):
    # for each docs, add an index in the metadata to be able to cite the sources
    for doc, index in zip(docs, range(len(docs)), strict=False):
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
