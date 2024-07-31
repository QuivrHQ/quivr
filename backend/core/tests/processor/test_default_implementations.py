import pytest

from quivr_core.files.file import FileExtension
from quivr_core.processor.processor_base import ProcessorBase


@pytest.mark.base
def test___build_processor():
    from langchain_community.document_loaders.base import BaseLoader

    from quivr_core.processor.implementations.default import _build_processor

    cls = _build_processor("TestCLS", BaseLoader, [FileExtension.txt])

    assert cls.__name__ == "TestCLS"
    assert issubclass(cls, ProcessorBase)
    assert "__init__" in cls.__dict__
    assert cls.supported_extensions == [FileExtension.txt]
    proc = cls()
    assert hasattr(proc, "loader_cls")
    # FIXME: proper mypy typing
    assert proc.loader_cls == BaseLoader  # type: ignore
