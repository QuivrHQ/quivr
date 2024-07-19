import pytest
from langchain_core.documents import Document

from quivr_core import registry
from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.processor.registry import (
    _import_class,
    get_processor_class,
    register_processor,
)
from quivr_core.processor.simple_txt_processor import SimpleTxtProcessor
from quivr_core.processor.tika_processor import TikaProcessor
from quivr_core.storage.file import FileExtension, QuivrFile


def test_get_processor_cls():
    cls = get_processor_class(FileExtension.txt)
    assert cls == SimpleTxtProcessor
    cls = get_processor_class(FileExtension.pdf)
    assert cls == TikaProcessor


def test__import_class():
    mod_path = "quivr_core.processor.tika_processor.TikaProcessor"
    mod = _import_class(mod_path)
    assert mod == TikaProcessor

    with pytest.raises(TypeError, match=r".* is not a class"):
        mod_path = "quivr_core.processor"
        _import_class(mod_path)

    with pytest.raises(TypeError, match=r".* ProcessorBase"):
        mod_path = "quivr_core.Brain"
        _import_class(mod_path)


def test_get_processor_cls_error():
    with pytest.raises(ValueError):
        get_processor_class(".docx")


def test_register_new_proc():
    nprocs = len(registry)

    class TestProcessor(ProcessorBase):
        supported_extensions = [".test"]

        async def process_file(self, file: QuivrFile) -> list[Document]:
            return []

    register_processor(".test", TestProcessor)
    assert len(registry) == nprocs + 1

    cls = get_processor_class(".test")
    assert cls == TestProcessor


def test_register_override_proc():
    class TestProcessor(ProcessorBase):
        supported_extensions = [".pdf"]

        async def process_file(self, file: QuivrFile) -> list[Document]:
            return []

    register_processor(".pdf", TestProcessor, override=True)
    cls = get_processor_class(FileExtension.pdf)
    assert cls == TestProcessor
