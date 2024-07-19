import importlib
import types
from typing import Type, TypedDict

from quivr_core.storage.file import FileExtension

from .processor_base import ProcessorBase

_registry: dict[str, Type[ProcessorBase]] = {}

# external, read only
registry = types.MappingProxyType(_registry)


class ProcEntry(TypedDict):
    cls_mod: str
    err: str | None


# Register based on mimetypes
known_processors: dict[FileExtension | str, ProcEntry] = {
    FileExtension.txt: ProcEntry(
        cls_mod="quivr_core.processor.simple_txt_processor.SimpleTxtProcessor",
        err="Please install quivr_core[base] to use TikTokenTxtProcessor ",
    ),
    FileExtension.pdf: ProcEntry(
        cls_mod="quivr_core.processor.tika_processor.TikaProcessor",
        err=None,
    ),
}


def get_processor_class(file_extension: FileExtension | str) -> Type[ProcessorBase]:
    """Fetch processor class from registry

    The dict ``known_processors`` maps file extensions to the locations
    of processors that could process them.
    Loading of these classes is *Lazy*. Appropriate import will happen
    the first time we try to process some file type.

    Some processors need additional dependencies. If the import fails
    we return the "err" field of the ProcEntry in  ``known_processors``.
    """

    if file_extension not in registry:
        if file_extension not in known_processors:
            raise ValueError(f"Extension not known: {file_extension}")
        entry = known_processors[file_extension]
        try:
            register_processor(file_extension, _import_class(entry["cls_mod"]))
        except ImportError as e:
            raise ImportError(entry["err"]) from e

    cls = registry[file_extension]
    return cls


def register_processor(
    file_type: FileExtension | str,
    proc_cls: str | Type[ProcessorBase],
    override: bool = False,
    errtxt=None,
):
    if isinstance(proc_cls, str):
        if file_type in known_processors and override is False:
            if proc_cls != known_processors[file_type]["cls_mod"]:
                raise ValueError(
                    f"Processor for ({file_type}) already in the registry and override is False"
                )
        else:
            known_processors[file_type] = ProcEntry(
                cls_mod=proc_cls,
                err=errtxt or f"{proc_cls} import failed for processor of {file_type}",
            )
    else:
        if file_type in registry and override is False:
            if _registry[file_type] is not proc_cls:
                raise ValueError(
                    f"Processor for ({file_type}) already in the registry and override is False"
                )
        else:
            _registry[file_type] = proc_cls


def _import_class(full_mod_path: str):
    if ":" in full_mod_path:
        mod_name, name = full_mod_path.rsplit(":", 1)
    else:
        mod_name, name = full_mod_path.rsplit(".", 1)

    mod = importlib.import_module(mod_name)

    for cls in name.split("."):
        mod = getattr(mod, cls)

    if not isinstance(mod, type):
        raise TypeError(f"{full_mod_path} is not a class")

    if not issubclass(mod, ProcessorBase):
        raise TypeError(f"{full_mod_path} is not a subclass of ProcessorBase ")

    return mod


def available_processors():
    """Return a list of the known processors."""
    return list(known_processors)
