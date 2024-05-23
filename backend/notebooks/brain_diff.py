import asyncio
import os
import pickle
import re
from pathlib import Path
from typing import List

import nest_asyncio
import pandas as pd
import uvloop
from llama_index.readers.file import MarkdownReader
from llama_parse import LlamaParse
from llama_parse.utils import Language, ResultType
from markdown_element import MarkdownElementNodeParser

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

def md_post_processing(src_text: str, min_length: int=40 , min_repetitions: int = 3) -> str:
    """
    Post-process OCR text to :
        - Remove repeated segments such as header and footer
        - Remove page breaks and page indications
        - Remove consecutive empty lines
        - delete spaces between tables
    """
    segments = src_text.split("\n") 
    repeated_segments = {}  

    for segment in segments:
        if len(segment) >= min_length and re.match(r'^\|( --- \|)*$', segment) is None:
            if segment in repeated_segments:
                repeated_segments[segment] += 1
            else:
                repeated_segments[segment] = 1

    segments_to_remove = []
    for segment, count in repeated_segments.items():
        if count >= min_repetitions:
            segments_to_remove.append(segment)

    cleaned_text = src_text
    for segment in segments_to_remove:
        cleaned_text = cleaned_text.replace(segment, "")

    cleaned_text = re.sub(r"^Page.*$", "\n", cleaned_text, flags=re.MULTILINE) #delete the entire line that start with "page .."
    cleaned_text =  re.sub(r"\n\n+", "\n\n", cleaned_text) #delete multiple new lines   
    cleaned_text =  re.sub(r"\n---\n","\n", cleaned_text) #delete the "---" that are present in the text (page jump)
    cleaned_text =  re.sub(r"\|\n+\|","|\n|", cleaned_text) #delete spaces between tables

    return cleaned_text 


def pdf2md(source_path: Path, post_process: bool = True, output_path : Path | None = None) -> List[str]:
    """Convert a PDF document to a markdown string."""
    parsing_instructions = """Do not take into account the page breaks (no --- between pages),
    do not repeat the header and the footer so the tables are merged. Keep the same format for similar tables. """

    parser = LlamaParse(
        api_key= str(os.getenv("LLAMA_CLOUD_API_KEY")),  
        result_type=ResultType.MD, 
        gpt4o_mode=True,
        verbose=True,
        language=Language.FRENCH, 
        parsing_instruction=parsing_instructions,
    )

    documents = parser.load_data(str(source_path))
    documents = [doc.get_content() for doc in documents]

    if post_process:
        documents = [md_post_processing(doc, min_length=5, min_repetitions=3) for doc in documents]
    
    if output_path:
        print("Saving the markdown file...")
        with open(output_path, "w") as f:
            for doc in documents:
                f.write(doc)
                f.write("\n\n")

    return documents

def get_nodes(src_path: Path, output_nodes_path: Path) :
    if not os.path.exists(output_nodes_path):
        reader = MarkdownReader()
        if src_path.suffix != ".md":
            raise ValueError("The source file should be a markdown file")
            
        documents = reader.load_data(src_path)
        node_parser = MarkdownElementNodeParser()
        
        raw_nodes = node_parser.get_nodes_from_documents(documents, show_progress= False)
        pickle.dump(raw_nodes, open(output_nodes_path, "wb"))

    else:
        raw_nodes = pickle.load(open(output_nodes_path, "rb"))
    
    return raw_nodes


if __name__ == "__main__":
    if not isinstance(asyncio.get_event_loop(), uvloop.Loop):
        nest_asyncio.apply()

    pdf_path = Path("./backend/notebooks/docs/CHARTE_QUALITE_PRODUIT2.pdf")
    md_path = Path("./backend/notebooks/docs/CHARTE_QUALITE_PRODUIT2.md")
    nodes_path = Path("./backend/notebooks/docs/charte.pkl")

    pdf2md(pdf_path, output_path = md_path)
    print("All_done!")

    doc_nodes = get_nodes(src_path = md_path, output_nodes_path= nodes_path)


