import asyncio
import os
import tempfile
from enum import Enum
from pathlib import Path

import streamlit as st
from diff_match_patch import diff_match_patch

# get environment variables
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from use_case_3.diff_type import DiffResult, llm_comparator
from use_case_3.llm_reporter import redact_report
from use_case_3.parser import DeadlyParser

load_dotenv()


class DocumentType(Enum):
    ETIQUETTE = "etiquette"
    CAHIER_DES_CHARGES = "cdc"


async def create_modification_report(
    before_file: str | Path,
    after_file: str | Path,
    type: DocumentType,
    llm: BaseChatModel,
    partition: bool = False,
    use_llm_comparator: bool = False,
    parser=DeadlyParser(),
) -> str:
    if type == DocumentType.ETIQUETTE:
        print("parsing before file")
        before_text = parser.deep_parse(before_file, partition=partition, llm=llm)
        print("parsing after file")
        after_text = parser.deep_parse(after_file, partition=partition, llm=llm)
    elif type == DocumentType.CAHIER_DES_CHARGES:
        before_text = await parser.aparse(before_file)
        after_text = await parser.aparse(after_file)

    print(before_text.page_content)
    print(after_text.page_content)
    text_after_sections = before_text.page_content.split("\n# ")
    text_before_sections = after_text.page_content.split("\n# ")
    assert len(text_after_sections) == len(text_before_sections)

    if use_llm_comparator:
        print("using llm comparator")
        return llm_comparator(
            before_text.page_content, after_text.page_content, llm=llm
        )
    print("using diff match patch")
    dmp = diff_match_patch()
    section_diffs = []
    for after_section, before_section in zip(
        text_after_sections, text_before_sections, strict=False
    ):
        main_diff: list[tuple[int, str]] = dmp.diff_main(after_section, before_section)
        section_diffs.append(DiffResult(main_diff))

    return redact_report(section_diffs, llm=llm)


def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
    ) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name


st.title("Document Modification Report Generator : Use Case 3")

# File uploaders
before_file = st.file_uploader("Upload 'Before' file", type=["pdf", "docx"])
after_file = st.file_uploader("Upload 'After' file", type=["pdf", "docx"])

# Document type selector
doc_type = st.selectbox("Select document type", ["ETIQUETTE", "CAHIER_DES_CHARGES"])

# Complexity of document
complexity = st.checkbox("Complex document (lot of text of OCRise)")

# Process button
if st.button("Process"):
    if before_file and after_file:
        with st.spinner("Processing files..."):
            # Save uploaded files
            before_path = save_uploaded_file(before_file)
            after_path = save_uploaded_file(after_file)

            # Initialize LLM
            openai_gpt4o = ChatOpenAI(
                model="gpt-4o",
                temperature=0,
                max_tokens=None,
                max_retries=2,
            )
            use_llm_comparator = True if doc_type == "ETIQUETTE" else False

            # Generate report
            print("generating report")
            report = asyncio.run(
                create_modification_report(
                    before_path,
                    after_path,
                    DocumentType[doc_type],
                    openai_gpt4o,
                    partition=complexity,
                    use_llm_comparator=use_llm_comparator,
                )
            )
            print("report generated")
            # Display results
            st.subheader("Modification Report")
            st.write(report)

            # Clean up temporary files
            os.unlink(before_path)
            os.unlink(after_path)
    else:
        st.error("Please upload both 'Before' and 'After' files.")
