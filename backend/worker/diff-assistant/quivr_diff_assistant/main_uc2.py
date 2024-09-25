import asyncio
from enum import Enum

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import UnstructuredElementNodeParser
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.schema import Document
from llama_index.llms.openai import OpenAI
from utils.utils import COMPARISON_PROMPT

from quivr_diff_assistant.use_case_3.parser import DeadlyParser

load_dotenv()

# Set pandas display options
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


def load_and_process_document(file_path, pickle_file):
    print(file_path)
    reader = SimpleDirectoryReader(input_files=[file_path])
    docs = reader.load_data()
    print(len(docs), " and", len(docs[0].text))
    if len(docs) == 1 and len(docs[0].text) < 9:
        print("No text found with classical parse, switching to OCR ...")
        parser = DeadlyParser()
        doc = parser.deep_parse(file_path)
        docs = [Document().from_langchain_format(doc)]

    node_parser = UnstructuredElementNodeParser()

    raw_nodes = node_parser.get_nodes_from_documents(docs)

    base_nodes, node_mappings = node_parser.get_base_nodes_and_mappings(raw_nodes)
    return base_nodes, node_mappings


def create_query_engine(base_nodes, node_mappings):
    vector_index = VectorStoreIndex(base_nodes)
    vector_retriever = vector_index.as_retriever(similarity_top_k=5)
    recursive_retriever = RecursiveRetriever(
        "vector",
        retriever_dict={"vector": vector_retriever},
        node_dict=node_mappings,
        verbose=True,
    )
    return RetrieverQueryEngine.from_args(
        recursive_retriever, llm=OpenAI(temperature=0, model="gpt-4")
    )


def compare_responses(response1, response2):
    llm = OpenAI(temperature=0, model="gpt-4")
    prompt = f"""
    Compare the following two responses and determine if they convey the same information:
    Response for document 1: {response1}
    Response for document 2: {response2}
    Are these responses essentially the same? Provide a brief explanation for your conclusion. The difference in format are not important, focus on the content and the numbers.
    If there are any specific differences, please highlight them with bullet points. Respond in french and in a markdown format.
    """
    return llm.complete(prompt)


class ComparisonTypes(str, Enum):
    CDC_ETIQUETTE = "Cahier des Charges - Etiquette"
    CDC_FICHE_DEV = "Cahier des Charges - Fiche Dev"


def llm_comparator(
    document: str, cdc: str, llm: BaseChatModel, comparison_type: ComparisonTypes
):
    chain = COMPARISON_PROMPT | llm | StrOutputParser()

    if comparison_type == ComparisonTypes.CDC_ETIQUETTE:
        text_1 = "Etiquette"
    elif comparison_type == ComparisonTypes.CDC_FICHE_DEV:
        text_1 = "Fiche Dev"

    return chain.stream(
        {
            "document": document,
            "text_1": text_1,
            "cdc": cdc,
            "text_2": "Cahier des Charges",
        }
    )


async def test_main():
    cdc_doc = "/Users/jchevall/Coding/diff-assistant/data/Use case #2/Cas2-2-1_Mendiant Lait_QD PC F03 - FR Cahier des charges produit -rev 2021-v2.pdf"
    doc = "/Users/jchevall/Coding/diff-assistant/data/Use case #2/Cas2-2-1_Proposition étiquette Mendiant Lait croustillant.pdf"

    cdc_doc = "/Users/jchevall/Coding/diff-assistant/data/Use case #2/Cas2-1-3_12_CDC_70690_Entremets rond vanille pécan individuel_2024.06.28 VALIDE.docx"
    doc = "/Users/jchevall/Coding/diff-assistant/data/Use case #2/Cas2-1-3_CDP_R&D_TABL_01_Fiche développement produit - Entremets vanille pécan 28 06 2024.xlsx"

    comparison_type = ComparisonTypes.CDC_FICHE_DEV

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.1,
        max_tokens=None,
        max_retries=2,
    )

    parser = DeadlyParser()
    parsed_cdc_doc = await parser.aparse(cdc_doc)

    if comparison_type == ComparisonTypes.CDC_ETIQUETTE:
        parsed_doc = await parser.deep_aparse(doc, llm=llm)
    else:
        parsed_doc = await parser.aparse(doc)

    print("\n\n Cahier des Charges")
    print(parsed_cdc_doc.page_content)

    print("\n\n Other document")
    print(parsed_doc.page_content)

    comparison = llm_comparator(
        document=parsed_doc.page_content,
        cdc=parsed_cdc_doc.page_content,
        llm=llm,
        comparison_type=comparison_type,
    )

    print("\n\n Comparison")
    print(comparison)


def get_document_path(doc):
    try:
        with open(doc.name, "wb") as temp_file:
            temp_file.write(doc.getbuffer())
        path = temp_file.name
    except:
        path = doc

    return path


async def parse_documents(cdc_doc, doc, comparison_type: ComparisonTypes, llm):
    parser = DeadlyParser()

    # Schedule the coroutines as tasks
    cdc_task = asyncio.create_task(parser.aparse(get_document_path(cdc_doc)))

    if comparison_type == ComparisonTypes.CDC_ETIQUETTE:
        doc_task = asyncio.create_task(
            parser.deep_aparse(get_document_path(doc), llm=llm)
        )
    else:
        doc_task = asyncio.create_task(parser.aparse(get_document_path(doc)))

    # Optionally, do other work here while tasks are running

    # Await the tasks to get the results
    parsed_cdc_doc = await cdc_task
    print("\n\n Cahier de Charges: \n", parsed_cdc_doc.page_content)

    parsed_doc = await doc_task
    print("\n\n Other doc: \n", parsed_doc.page_content)

    return parsed_cdc_doc, parsed_doc


def main():
    st.title("Document Comparison Tool : Use Case 2")

    # File uploaders for two documents
    cdc_doc = st.file_uploader(
        "Upload Cahier des Charges", type=["docx", "xlsx", "pdf", "txt"]
    )
    doc = st.file_uploader(
        "Upload Etiquette / Fiche Dev", type=["docx", "xlsx", "pdf", "txt"]
    )

    comparison_type = st.selectbox(
        "Select document types",
        [ComparisonTypes.CDC_ETIQUETTE.value, ComparisonTypes.CDC_FICHE_DEV.value],
    )

    if st.button("Process Documents and Questions"):
        if not cdc_doc or not doc:
            st.error("Please upload both documents before launching the processing.")
            return

        with st.spinner("Processing files..."):
            llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0.1,
                max_tokens=None,
                max_retries=2,
            )

            parsed_cdc_doc, parsed_doc = asyncio.run(
                parse_documents(cdc_doc, doc, comparison_type=comparison_type, llm=llm)
            )

            comparison = llm_comparator(
                document=parsed_doc.page_content,
                cdc=parsed_cdc_doc.page_content,
                llm=llm,
                comparison_type=comparison_type,
            )
            # Run the async function using asyncio.run()
            # comparison = asyncio.run(process_documents(cdc_doc, doc, comparison_type))
            st.write_stream(comparison)


if __name__ == "__main__":
    main()
