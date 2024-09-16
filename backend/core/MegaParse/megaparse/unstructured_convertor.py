import re
from enum import Enum

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from unstructured.partition.pdf import partition_pdf


class ModelEnum(str, Enum):
    """Model to use for the conversion"""

    LOCAL = "llama3"
    GPT4O = "gpt-4o"
    NONE = None


class UnstructuredParser:
    load_dotenv()

    # Function to convert element category to markdown format
    def convert_to_markdown(self, elements):
        markdown_content = ""
        element_hierarchy = {}

        for el in elements:
            markdown_content += self.get_markdown_line(el)

        return markdown_content

    def get_markdown_line(self, el):
        element_type = el["type"]
        text = el["text"]
        metadata = el["metadata"]
        parent_id = metadata.get("parent_id", None)
        category_depth = metadata.get("category_depth", 0)
        if "emphasized_text_contents" in metadata:
            print(metadata["emphasized_text_contents"])

        markdown_line = ""

        if element_type == "Title":
            if parent_id:
                markdown_line = (
                    f"## {text}\n\n"  # Adjusted to add sub headers if parent_id exists
                )
            else:
                markdown_line = f"# {text}\n\n"
        elif element_type == "Subtitle":
            markdown_line = f"## {text}\n\n"
        elif element_type == "Header":
            markdown_line = f"{'#' * (category_depth + 1)} {text}\n\n"
        elif element_type == "Footer":
            markdown_line = f"#### {text}\n\n"
        elif element_type == "NarrativeText":
            markdown_line = f"{text}\n\n"
        elif element_type == "ListItem":
            markdown_line = f"- {text}\n"
        elif element_type == "Table":
            markdown_line = el["metadata"]["text_as_html"]
        elif element_type == "PageBreak":
            markdown_line = "---\n\n"
        elif element_type == "Image":
            markdown_line = f"![Image]({el['metadata'].get('image_path', '')})\n\n"
        elif element_type == "Formula":
            markdown_line = f"$$ {text} $$\n\n"
        elif element_type == "FigureCaption":
            markdown_line = f"**Figure:** {text}\n\n"
        elif element_type == "Address":
            markdown_line = f"**Address:** {text}\n\n"
        elif element_type == "EmailAddress":
            markdown_line = f"**Email:** {text}\n\n"
        elif element_type == "CodeSnippet":
            markdown_line = f"```{el['metadata'].get('language', '')}\n{text}\n```\n\n"
        elif element_type == "PageNumber":
            markdown_line = f"**Page {text}**\n\n"
        else:
            markdown_line = f"{text}\n\n"

        return markdown_line

    def partition_pdf_file(self, path, strategy="fast"):
        return partition_pdf(
            filename=path, infer_table_structure=True, strategy=strategy
        )

    def improve_layout(
        self, elements, remove_repeated_headers=True, model: ModelEnum = ModelEnum.GPT4O
    ):
        llm = None
        chain = None
        if model != ModelEnum.NONE:
            llm = (
                ChatOpenAI(model="gpt-4o", temperature=0.1)
                if model == ModelEnum.GPT4O
                else ChatOllama(model=model.value, temperature=0.1)
            )

            # Define the prompt
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "human",
                        """You are an expert in markdown tables, match this text and this html table to fill a md table. You answer with just the table in pure markdown, nothing else.
                    <TEXT>
                    {text}
                    </TEXT>
                    <HTML>
                    {html}
                    </HTML>

                    Note, the previous table (that might be related since appearing just before):
                    <PREVIOUS_TABLE>
                    {previous_table}
                    </PREVIOUS_TABLE>""",
                    ),
                ]
            )
            chain = prompt | llm

        table_stack: list[str] = []

        improved_elements = []
        for el in elements:
            if el.category == "Table":
                if el.text not in set(table_stack):
                    if chain:
                        result = chain.invoke(
                            {
                                "text": el.text,
                                "html": el.metadata.text_as_html,
                                "previous_table": table_stack[-1]
                                if table_stack
                                else "",
                            }
                        )
                        cleaned_result = result.content
                        cleaned_content = re.sub(
                            r"^```.*$\n?", "", str(cleaned_result), flags=re.MULTILINE
                        )
                    else:
                        cleaned_content = el.text

                    el.metadata.text_as_html = f"[TABLE]\n{cleaned_content}\n[/TABLE]"
                    # add line break to separate tables
                    el.metadata.text_as_html = el.metadata.text_as_html + "\n\n"  # type: ignore
                    table_stack.append(el.text)
                    improved_elements.append(el)

            elif el.category not in ["Header", "Footer"]:
                if "page" not in el.text.lower():
                    if (
                        el.text not in set(table_stack)
                        and "page" not in el.text.lower()
                    ) or remove_repeated_headers == False:
                        improved_elements.append(el)

                    table_stack.append(el.text.strip())
                    table_stack.append("")

        return improved_elements

    def convert(self, path, model: ModelEnum = ModelEnum.GPT4O, strategy="fast"):
        # Partition the PDF
        elements = self.partition_pdf_file(path, strategy=strategy)

        # Improve table elements
        improved_elements = self.improve_layout(elements, model=model)

        elements_dict = [el.to_dict() for el in improved_elements]
        markdown_content = self.convert_to_markdown(elements_dict)
        return markdown_content


# if __name__ == "__main__":
#     parser = UnstructuredParser()
#     response = parser.convert("megaparse/tests/input_tests/MegaFake_report.pdf", model=ModelEnum.NONE)
#     print(response)
#     with open("megaparse/tests/output_tests/cdp.md", "w") as f:
#         f.write(response)
#     print("ok")
