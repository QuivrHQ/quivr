from typing import Dict, List, Tuple

from langchain.schema import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    format_document,
)

# TODO(@aminediro): define a types packages where we clearly define IO types
# This should be used for serialization/deseriallization later
from backend.modules.brain.rags.quivr_rag import DEFAULT_DOCUMENT_PROMPT
from backend.modules.chat.dto.outputs import GetChatHistoryOutput
from backend.modules.knowledge.entity.knowledge import Knowledge
from backend.packages.quivr_core.models import (
    ParsedRAGResponse,
    RAGResponseMetadata,
    RawRAGResponse,
)


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


def format_file_list(list_files_array: list[Knowledge], max_files: int = 20) -> str:
    list_files = [file.file_name or file.url for file in list_files_array]
    files: list[str] = list(filter(lambda n: n is not None, list_files))  # type: ignore
    files = files[:max_files]

    files_str = "\n".join(files) if list_files_array else "None"
    return files_str
