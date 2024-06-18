from typing import Any, Dict, List, Tuple
from uuid import UUID

from langchain.schema import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    format_document,
)

from backend.logger import get_logger

# TODO(@aminediro): define a types packages where we clearly define IO types
# This should be used for serialization/deseriallization later
from backend.modules.brain.rags.quivr_rag import DEFAULT_DOCUMENT_PROMPT
from backend.modules.chat.dto.chats import Sources
from backend.modules.chat.dto.outputs import GetChatHistoryOutput
from backend.modules.knowledge.entity.knowledge import Knowledge
from backend.modules.upload.service.generate_file_signed_url import (
    generate_file_signed_url,
)
from backend.packages.quivr_core.models import (
    ParsedRAGChunkResponse,
    ParsedRAGResponse,
    RAGResponseMetadata,
    RawRAGResponse,
)

logger = get_logger(__name__)


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


# TODO: CONVOLUTED LOGIC !
# TODO(@aminediro): redo this
def parse_chunk_response(
    rolling_answer: Any,
    response_tokens: str,
    raw_chunk: Any,
    supports_func_calling: bool,
) -> ParsedRAGChunkResponse:

    # Init with sources
    metadata = {"sources": raw_chunk["docs"] if "docs" in raw_chunk else []}

    if supports_func_calling:
        # TODO: What is this assignment ?
        rolling_answer += raw_chunk["answer"]
        if (
            rolling_answer.tool_calls
            and rolling_answer.tool_calls[-1].get("args")
            and "answer" in rolling_answer.tool_calls[-1]["args"]
        ):
            # Only send the difference between answer and response_tokens which was the previous answer
            answer = rolling_answer.tool_calls[-1]["args"]["answer"]
            # TODO(@aminediro) : WHYYY THIS  here?!?
            difference: str = answer[len(response_tokens) :]
            response_tokens += answer
            if (
                rolling_answer.tool_calls
                and rolling_answer.tool_calls[-1].get("args")
                and "citations" in rolling_answer.tool_calls[-1]["args"]
            ):
                citations = rolling_answer.tool_calls[-1]["args"]["citations"]
                metadata["citations"] = citations
            if (
                rolling_answer.tool_calls
                and rolling_answer.tool_calls[-1].get("args")
                and "followup_questions" in rolling_answer.tool_calls[-1]["args"]
            ):
                followup_questions = rolling_answer.tool_calls[-1]["args"][
                    "followup_questions"
                ]
                metadata["followup_questions"] = followup_questions
            if (
                rolling_answer.tool_calls
                and rolling_answer.tool_calls[-1].get("args")
                and "thoughts" in rolling_answer.tool_calls[-1]["args"]
            ):
                thoughts = rolling_answer.tool_calls[-1]["args"]["thoughts"]
                metadata["thoughts"] = thoughts
        return ParsedRAGChunkResponse(
            answer=difference, metadata=RAGResponseMetadata(**metadata)
        )
    else:
        response_tokens += raw_chunk["answer"].content
        return ParsedRAGChunkResponse(
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


def format_file_list(list_files_array: list[Knowledge], max_files: int = 20) -> str:
    list_files = [file.file_name or file.url for file in list_files_array]
    files: list[str] = list(filter(lambda n: n is not None, list_files))  # type: ignore
    files = files[:max_files]

    files_str = "\n".join(files) if list_files_array else "None"
    return files_str


# TODO: REFACTOR THIS
def generate_source(
    source_documents: List[Any] | None,
    brain_id: UUID,
    citations: List[int] | None = None,
) -> List[Sources]:
    """
    Generate the sources list for the answer
    It takes in a list of sources documents and citations that points to the docs index that was used in the answer
    """
    # Initialize an empty list for sources
    sources_list: List[Sources] = []

    # Initialize a dictionary for storing generated URLs
    generated_urls = {}

    # remove duplicate sources with same name and create a list of unique sources
    sources_url_cache = {}

    # Get source documents from the result, default to an empty list if not found
    # If source documents exist
    if source_documents:
        logger.info(f"Citations {citations}")
        # Iterate over each document
        for doc, index in zip(source_documents, range(len(source_documents))):
            logger.info(f"Processing source document {doc.metadata['file_name']}")
            if citations is not None:
                if index not in citations:
                    logger.info(f"Skipping source document {doc.metadata['file_name']}")
                    continue
            # Check if 'url' is in the document metadata
            is_url = (
                "original_file_name" in doc.metadata
                and doc.metadata["original_file_name"] is not None
                and doc.metadata["original_file_name"].startswith("http")
            )

            # Determine the name based on whether it's a URL or a file
            name = (
                doc.metadata["original_file_name"]
                if is_url
                else doc.metadata["file_name"]
            )

            # Determine the type based on whether it's a URL or a file
            type_ = "url" if is_url else "file"

            # Determine the source URL based on whether it's a URL or a file
            if is_url:
                source_url = doc.metadata["original_file_name"]
            else:
                file_path = f"{brain_id}/{doc.metadata['file_name']}"
                # Check if the URL has already been generated
                if file_path in generated_urls:
                    source_url = generated_urls[file_path]
                else:
                    # Generate the URL
                    if file_path in sources_url_cache:
                        source_url = sources_url_cache[file_path]
                    else:
                        generated_url = generate_file_signed_url(file_path)
                        if generated_url is not None:
                            source_url = generated_url.get("signedURL", "")
                        else:
                            source_url = ""
                    # Store the generated URL
                    generated_urls[file_path] = source_url

            # Append a new Sources object to the list
            sources_list.append(
                Sources(
                    name=name,
                    type=type_,
                    source_url=source_url,
                    original_file_name=name,
                    citation=doc.page_content,
                )
            )
    else:
        logger.info("No source documents found or source_documents is not a list.")
    return sources_list
