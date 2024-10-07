import os
import random
import string
import tempfile
from enum import Enum
from pathlib import Path

from diff_match_patch import diff_match_patch

# get environment variables
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from quivr_api.logger import get_logger
from quivr_api.modules.assistant.dto.inputs import InputAssistant
from quivr_api.modules.assistant.services.tasks_service import TasksService
from quivr_api.modules.dependencies import get_supabase_client
from quivr_diff_assistant.use_case_3.diff_type import DiffResult, llm_comparator
from quivr_diff_assistant.use_case_3.llm_reporter import redact_report
from quivr_diff_assistant.use_case_3.parser import DeadlyParser

logger = get_logger(__name__)


class DocumentType(Enum):
    ETIQUETTE = "etiquette"
    CAHIER_DES_CHARGES = "cdc"


async def process_cdp_use_case_3(
    assistant_id: str,
    notification_uuid: str,
    task_id: int,
    tasks_service: TasksService,
    user_id: str,
) -> str:
    task = await tasks_service.get_task_by_id(task_id, user_id)  # type: ignore

    # Parse settings into InputAssistant
    input_assistant = InputAssistant.model_validate(task.settings)
    assert input_assistant.inputs.files is not None
    assert len(input_assistant.inputs.files) == 2

    # Get the value of the "Document 1" key and "Document 2" key. The input files might not be in the order of "Document 1" and "Document 2"
    # So we need to find the correct order
    before_file_key = input_assistant.inputs.files[0].key
    after_file_key = input_assistant.inputs.files[1].key

    before_file_value = input_assistant.inputs.files[0].value
    after_file_value = input_assistant.inputs.files[1].value

    if before_file_key == "Document 2":
        before_file_value = input_assistant.inputs.files[1].value
        after_file_value = input_assistant.inputs.files[0].value

    # Get the files from supabase
    supabase_client = get_supabase_client()
    path = f"{task.assistant_id}/{task.pretty_id}/"

    await tasks_service.update_task(task_id, {"status": "processing"})

    # Before file key - parsed from the
    before_file_data = supabase_client.storage.from_("quivr").download(
        f"{path}{before_file_value}"
    )
    after_file_data = supabase_client.storage.from_("quivr").download(
        f"{path}{after_file_value}"
    )

    # Generate a random string of 8 characters
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=8))

    # Write temp files with the original name without using save_uploaded_file
    # because the file is already in the quivr bucket
    before_file_path = f"/tmp/{random_string}_{before_file_value}"
    after_file_path = f"/tmp/{random_string}_{after_file_value}"
    with open(before_file_path, "wb") as f:
        f.write(before_file_data)
    with open(after_file_path, "wb") as f:
        f.write(after_file_data)

    assert input_assistant.inputs.select_texts is not None
    value_use_case = input_assistant.inputs.select_texts[0].value

    ## Get the document type
    document_type = None
    if value_use_case == "Etiquettes":
        document_type = DocumentType.ETIQUETTE
    elif value_use_case == "Cahier des charges":
        document_type = DocumentType.CAHIER_DES_CHARGES
    else:
        raise ValueError(f"Invalid value for use case: {value_use_case}")

    ## Get the hard to read document boolean value
    assert input_assistant.inputs.booleans is not None
    hard_to_read_document = input_assistant.inputs.booleans[0].value

    assert before_file_data is not None
    assert after_file_data is not None

    openai_gpt4o = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_tokens=None,
        max_retries=2,
    )

    llm_comparator = True if document_type == DocumentType.ETIQUETTE else False
    report = await create_modification_report(
        before_file=before_file_path,
        after_file=after_file_path,
        type=document_type,
        llm=openai_gpt4o,
        partition=hard_to_read_document,
        use_llm_comparator=llm_comparator,
    )

    os.unlink(before_file_path)
    os.unlink(after_file_path)
    return report


async def create_modification_report(
    before_file: str | Path | bytes,
    after_file: str | Path | bytes,
    type: DocumentType,
    llm: BaseChatModel,
    partition: bool = False,
    use_llm_comparator: bool = False,
    parser=DeadlyParser(),
) -> str:
    if type == DocumentType.ETIQUETTE:
        logger.debug("parsing before file")
        before_text = parser.deep_parse(before_file, partition=partition, llm=llm)
        logger.debug("parsing after file")
        after_text = parser.deep_parse(after_file, partition=partition, llm=llm)
    elif type == DocumentType.CAHIER_DES_CHARGES:
        before_text = await parser.aparse(before_file)
        after_text = await parser.aparse(after_file)

    logger.debug(before_text.page_content)
    logger.debug(after_text.page_content)
    text_after_sections = before_text.page_content.split("\n# ")
    text_before_sections = after_text.page_content.split("\n# ")

    if use_llm_comparator:
        logger.debug("using llm comparator")
        llm_comparator_result = llm_comparator(
            before_text.page_content, after_text.page_content, llm=llm
        )
        return llm_comparator_result
    logger.debug("using diff match patch")
    dmp = diff_match_patch()
    section_diffs = []
    for after_section, before_section in zip(
        text_after_sections, text_before_sections, strict=False
    ):
        main_diff: list[tuple[int, str]] = dmp.diff_main(after_section, before_section)
        section_diffs.append(DiffResult(main_diff))

    logger.debug(section_diffs)
    report = redact_report(section_diffs, llm=llm)
    return report


def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
    ) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name


# st.title("Document Modification Report Generator : Use Case 3")

# # File uploaders
# before_file = st.file_uploader("Upload 'Before' file", type=["pdf", "docx"])
# after_file = st.file_uploader("Upload 'After' file", type=["pdf", "docx"])

# # Document type selector
# doc_type = st.selectbox("Select document type", ["ETIQUETTE", "CAHIER_DES_CHARGES"])

# # Complexity of document
# complexity = st.checkbox("Complex document (lot of text of OCRise)")

# # Process button
# if st.button("Process"):
#     if before_file and after_file:
#         with st.spinner("Processing files..."):
#             # Save uploaded files
#             before_path = save_uploaded_file(before_file)
#             after_path = save_uploaded_file(after_file)

#             # Initialize LLM
#             openai_gpt4o = ChatOpenAI(
#                 model="gpt-4o",
#                 temperature=0,
#                 max_tokens=None,
#                 max_retries=2,
#             )
#             use_llm_comparator = True if doc_type == "ETIQUETTE" else False

#             # Generate report
#             logger.debug("generating report")
#             report = asyncio.run(
#                 create_modification_report(
#                     before_path,
#                     after_path,
#                     DocumentType[doc_type],
#                     openai_gpt4o,
#                     partition=complexity,
#                     use_llm_comparator=use_llm_comparator,
#                 )
#             )
#             logger.debug("report generated")
#             # Display results
#             st.subheader("Modification Report")
#             st.write(report)

#             # Clean up temporary files
#             os.unlink(before_path)
#             os.unlink(after_path)
#     else:
#         st.error("Please upload both 'Before' and 'After' files.")
