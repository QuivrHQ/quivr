from docx.document import Document as DocumentObject
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.section import Section
from docx.section import _Footer as Footer
from docx.section import _Header as Header
from docx.table import Table
from docx.text.paragraph import Paragraph


def print_element(element):
    if isinstance(element, Paragraph):
        # Print the paragraph text
        print(f"Paragraph: {element.text}")
    elif isinstance(element, Table):
        # Print the table content
        print("Table:")
        for row in element.rows:
            for cell in row.cells:
                print(cell.text, end="\t")
            print()
    elif isinstance(element, Section):
        # Print section properties
        print("Section:")
        print(f"  Start type: {element.start_type}")
        print(f"  Page height: {element.page_height}")
        print(f"  Page width: {element.page_width}")
    elif isinstance(element, Header):
        # Print header content
        print("Header:")
        for paragraph in element.paragraphs:
            print(f"  {paragraph.text}")
    elif isinstance(element, Footer):
        # Print footer content
        print("Footer:")
        for paragraph in element.paragraphs:
            print(f"  {paragraph.text}")
    else:
        print(f"Unknown element: {type(element)}")


def print_docx(doc: DocumentObject) -> None:
    for element in doc.element.body:
        if isinstance(element, CT_P):  # Paragraph
            print_element(Paragraph(element, doc))
        elif isinstance(element, CT_Tbl):  # Table
            print_element(Table(element, doc))
