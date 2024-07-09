import os

from fpdf import FPDF
from pydantic import BaseModel


class PDFModel(BaseModel):
    title: str
    content: str


class PDFGenerator(FPDF):
    def __init__(self, pdf_model: PDFModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pdf_model = pdf_model
        self.add_font(
            "DejaVu",
            "",
            os.path.join(os.path.dirname(__file__), "font/DejaVuSansCondensed.ttf"),
            uni=True,
        )
        self.add_font(
            "DejaVu",
            "B",
            os.path.join(
                os.path.dirname(__file__), "font/DejaVuSansCondensed-Bold.ttf"
            ),
            uni=True,
        )
        self.add_font(
            "DejaVu",
            "I",
            os.path.join(
                os.path.dirname(__file__), "font/DejaVuSansCondensed-Oblique.ttf"
            ),
        )

    def header(self):
        # Logo
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        self.image(logo_path, 10, 10, 20)  # Adjust size as needed

        # Move cursor to right of image
        self.set_xy(20, 15)

        # Title
        self.set_font("DejaVu", "B", 12)
        self.multi_cell(0, 10, self.pdf_model.title, align="C")
        self.ln(5)  # Padding after title

    def footer(self):
        self.set_y(-15)

        self.set_font("DejaVu", "I", 8)
        self.set_text_color(169, 169, 169)
        self.cell(80, 10, "Generated by Quivr", 0, 0, "C")
        self.set_font("DejaVu", "U", 8)
        self.set_text_color(0, 0, 255)
        self.cell(30, 10, "quivr.app", 0, 0, "C", link="https://quivr.app")
        self.cell(0, 10, "Github", 0, 1, "C", link="https://github.com/quivrhq/quivr")

    def chapter_body(self):
        self.set_font("DejaVu", "", 12)
        self.multi_cell(0, 10, self.pdf_model.content, markdown=True)
        self.ln()

    def print_pdf(self):
        self.add_page()
        self.chapter_body()


if __name__ == "__main__":
    pdf_model = PDFModel(
        title="Summary of Legal Services Rendered by Orrick",
        content="""
**Summary:**
The document is an invoice from Quivr Technologies, Inc. for legal services provided to client YC W24, related to initial corporate work. The total fees and disbursements amount to $8,345.00 for services rendered through February 29, 2024. The invoice includes specific instructions for payment remittance and contact information for inquiries. Online payment through e-billexpress.com is also an option.

**Key Points:**
- Quivr Technologies, Inc., based in France and represented by Stanislas Girard, provided legal services to client YC W24.
- Services included preparing and completing forms, drafting instructions, reviewing and responding to emails, filing 83(b) elections, and finalizing documents for submission to YC.
- The timekeepers involved in providing these services were Julien Barbey, Maria T. Coladonato, Michael LaBlanc, Jessy K. Parker, Marisol Sandoval Villasenor, Alexis A. Smith, and Serena Tibrewala.
- The total hours billed for the services provided was 16.20, with a total cost of $8,345.00.
- Instructions for payment remittance, contact information, and online payment options through e-billex
""",
    )
    pdf = PDFGenerator(pdf_model)
    pdf.print_pdf()
    pdf.output("simple.pdf")
