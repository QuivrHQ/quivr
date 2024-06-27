import os
from tempfile import NamedTemporaryFile

import pytest
from langchain_community.document_loaders import UnstructuredPDFLoader
from quivr_api.models.files import File


@pytest.fixture
def pdf_file():
    file_path = "tests/file_process/dummy.pdf"
    file_name = os.path.basename(file_path)
    with NamedTemporaryFile(
        suffix="_" + file_name,  # pyright: ignore reportPrivateUsage=none
    ) as tmp_file:
        with open(file_path, "rb") as f:
            content = f.read()
            tmp_file.write(content)
        tmp_file.flush()
        yield File(
            file_name="dummy",
            tmp_file_path=tmp_file.name,
            file_extension="pdf",
            bytes_content=content,
            file_size=len(content),
        )


def test_pdf_process(pdf_file):
    pdf_file.compute_documents(UnstructuredPDFLoader)

    assert len(pdf_file.documents) > 0
    assert pdf_file.documents[0].page_content == "Dummy PDF download"
