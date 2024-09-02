import logging
from heapq import heappop

import pytest
from langchain_core.documents import Document
from quivr_core import registry
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.implementations.simple_txt_processor import SimpleTxtProcessor
from quivr_core.processor.implementations.tika_processor import TikaProcessor
from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.processor.registry import (
    _LOWEST_PRIORITY,
    ProcEntry,
    ProcMapping,
    _append_proc_mapping,
    _import_class,
    available_processors,
    get_processor_class,
    known_processors,
    register_processor,
)


# TODO : reimplement when quivr-core will be its own package
@pytest.mark.skip(reason="TODO: reimplement when quivr-core will be its own package")
def test_get_default_processors_cls():
    from quivr_core.processor.implementations.default import TikTokenTxtProcessor

    cls = get_processor_class(FileExtension.txt)
    assert cls == TikTokenTxtProcessor

    cls = get_processor_class(FileExtension.pdf)
    # FIXME: using this class will actually fail if you don't have the
    assert cls == TikaProcessor


@pytest.mark.skip(reason="TODO: reimplement when quivr-core will be its own package")
def test_get_default_processors_cls_core():
    cls = get_processor_class(FileExtension.txt)
    assert cls == SimpleTxtProcessor

    cls = get_processor_class(FileExtension.pdf)
    assert cls == TikaProcessor


def test_append_proc_mapping_empty():
    proc_mapping = {}

    _append_proc_mapping(
        proc_mapping,
        file_ext=FileExtension.txt,
        cls_mod="test.test",
        errtxt="error",
        priority=None,
    )
    assert len(proc_mapping) == 1
    assert len(proc_mapping[FileExtension.txt]) == 1
    assert proc_mapping[FileExtension.txt][0] == ProcEntry(
        priority=_LOWEST_PRIORITY, cls_mod="test.test", err="error"
    )


def test_append_proc_mapping_priority():
    proc_mapping: ProcMapping = {
        FileExtension.txt: [
            ProcEntry(
                cls_mod="quivr_core.processor.implementations.simple_txt_processor.SimpleTxtProcessor",
                err=None,
                priority=_LOWEST_PRIORITY,
            )
        ],
    }
    _append_proc_mapping(
        proc_mapping,
        file_ext=FileExtension.txt,
        cls_mod="test.test",
        errtxt="error",
        priority=0,
    )

    assert len(proc_mapping[FileExtension.txt]) == 2
    # Procs are appended in order
    assert heappop(proc_mapping[FileExtension.txt]) == ProcEntry(
        priority=0, cls_mod="test.test", err="error"
    )


def test_append_proc_mapping():
    proc_mapping: ProcMapping = {
        FileExtension.txt: [
            ProcEntry(
                cls_mod="quivr_core.processor.implementations.simple_txt_processor.SimpleTxtProcessor",
                err=None,
                priority=_LOWEST_PRIORITY,
            )
        ],
    }
    _append_proc_mapping(
        proc_mapping,
        file_ext=FileExtension.txt,
        cls_mod="test.test",
        errtxt="error",
        priority=None,
    )

    assert len(proc_mapping[FileExtension.txt]) == 2
    # Procs are appended in order
    assert heappop(proc_mapping[FileExtension.txt]) == ProcEntry(
        priority=_LOWEST_PRIORITY - 1, cls_mod="test.test", err="error"
    )
    assert heappop(proc_mapping[FileExtension.txt]) == ProcEntry(
        cls_mod="quivr_core.processor.implementations.simple_txt_processor.SimpleTxtProcessor",
        err=None,
        priority=_LOWEST_PRIORITY,
    )


@pytest.mark.skip(
    reason="TODO: audio processors will be added to quivr-core very soon!"
)
def test_known_processors():
    assert all(
        ext in known_processors for ext in list(FileExtension)
    ), "base-env : Some file extensions don't have a default processor"


def test__import_class():
    mod_path = "quivr_core.processor.implementations.tika_processor.TikaProcessor"
    mod = _import_class(mod_path)
    assert mod == TikaProcessor

    with pytest.raises(TypeError, match=r".* is not a class"):
        mod_path = "quivr_core.processor"
        _import_class(mod_path)

    with pytest.raises(TypeError, match=r".* ProcessorBase"):
        mod_path = "quivr_core.Brain"
        _import_class(mod_path)


@pytest.mark.skip(reason="TODO: reimplement when quivr-core will be its own package")
def test_get_processor_cls_import_error(caplog):
    """
    Test in an environement where we only have the bare minimum parsers.
    The .html can't be parsed so we should raise an ImportError"""
    with pytest.raises(ImportError):
        get_processor_class(".html")


def test_get_processor_cls_error():
    with pytest.raises(ValueError):
        get_processor_class(".sdfkj")


@pytest.mark.skip("needs tox for separating side effects on other tests")
def test_register_new_proc_noappend():
    with pytest.raises(ValueError):
        register_processor(FileExtension.txt, "test.", append=False)


@pytest.mark.skip("needs tox for separating side effects on other tests")
def test_register_new_proc_append(caplog):
    n = len(known_processors[FileExtension.txt])
    register_processor(FileExtension.txt, "test.", append=True)
    assert len(known_processors[FileExtension.txt]) == n + 1

    with caplog.at_level(logging.INFO, logger="quivr_core"):
        register_processor(FileExtension.txt, "test.", append=True)
        assert caplog.record_tuples == [
            ("quivr_core", logging.INFO, "test. already in registry...")
        ]


@pytest.mark.skip("needs tox for separating side effects on other tests")
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


def test_register_non_processor():
    class NOTPROC:
        supported_extensions = [".pdf"]

    with pytest.raises(AssertionError):
        register_processor(".pdf", NOTPROC)  # type: ignore


def test_register_override_proc():
    class TestProcessor(ProcessorBase):
        supported_extensions = [".pdf"]

        @property
        def processor_metadata(self):
            return {}

        async def process_file_inner(self, file: QuivrFile) -> list[Document]:
            return []

    register_processor(".pdf", TestProcessor, override=True)
    cls = get_processor_class(FileExtension.pdf)
    assert cls == TestProcessor


def test_register_override_error():
    # Register class to pdf
    _ = get_processor_class(FileExtension.pdf)

    class TestProcessor(ProcessorBase):
        supported_extensions = [FileExtension.pdf]

        @property
        def processor_metadata(self):
            return {}

        async def process_file_inner(self, file: QuivrFile) -> list[Document]:
            return []

    with pytest.raises(ValueError):
        register_processor(".pdf", TestProcessor, override=False)


def test_available_processors():
    assert 17 == len(available_processors())
