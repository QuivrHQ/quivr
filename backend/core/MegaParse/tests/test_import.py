import pytest
from megaparse.Converter import MegaParse


@pytest.mark.skip("slow test")
def test_load():
    megaparse = MegaParse(file_path="./tests/data/dummy.pdf")
    element = megaparse.load()
    assert element.page_content.strip("\n") == "# Dummy PDF download"
