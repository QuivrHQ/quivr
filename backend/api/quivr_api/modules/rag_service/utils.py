import logging
from typing import Any, List
from uuid import UUID

from quivr_api.modules.chat.dto.chats import Sources
from quivr_api.modules.upload.service.generate_file_signed_url import (
    generate_file_signed_url,
)

logger = logging.getLogger(__name__)


# TODO: REFACTOR THIS, it does call the DB , so maybe in a service
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
        logger.debug(f"Citations {citations}")
        for index, doc in enumerate(source_documents):
            logger.debug(f"Processing source document {doc.metadata['file_name']}")
            if citations is not None:
                if index not in citations:
                    logger.debug(
                        f"Skipping source document {doc.metadata['file_name']}"
                    )
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
                    integration=doc.metadata["integration"],
                    integration_link=doc.metadata["integration_link"],
                )
            )
    else:
        logger.debug("No source documents found or source_documents is not a list.")
    return sources_list
