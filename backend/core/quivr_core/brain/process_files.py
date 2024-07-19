import logging
from typing import Any

from langchain_core.documents import Document

from quivr_core.processor.registry import get_processor_class
from quivr_core.storage.storage_base import StorageBase

logger = logging.getLogger("quivr_core")


async def process_files(
    storage: StorageBase, skip_file_error: bool, **processor_kwargs: dict[str, Any]
) -> list[Document]:
    knowledge = []
    for file in await storage.get_files():
        try:
            if file.file_extension:
                processor_cls = get_processor_class(file.file_extension)
                logger.debug(f"processing {file} using class {processor_cls.__name__}")
                processor = processor_cls(**processor_kwargs)
                docs = await processor.process_file(file)
                knowledge.extend(docs)
            else:
                logger.error(f"can't find processor for {file}")
                if skip_file_error:
                    continue
                else:
                    raise ValueError(f"can't parse {file}. can't find file extension")
        except KeyError as e:
            if skip_file_error:
                continue
            else:
                raise Exception(f"Can't parse {file}. No available processor") from e

    return knowledge
