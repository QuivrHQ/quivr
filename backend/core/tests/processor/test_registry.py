import pytest

from quivr_core.processor.registry import _import_class, get_processor_class
from quivr_core.processor.simple_txt_processor import SimpleTxtProcessor
from quivr_core.processor.tika_processor import TikaProcessor
from quivr_core.storage.file import FileExtension


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


# def test_register():
#     print()
#     pass
