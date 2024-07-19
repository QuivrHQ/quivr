import importlib
import logging
import types
from dataclasses import dataclass, field
from heapq import heappop, heappush
from typing import Type, TypeAlias

from quivr_core.files.file import FileExtension
from quivr_core.processor.implementations.default import (
    BibTexProcessor,
    CSVProcessor,
    DOCXProcessor,
    EpubProcessor,
    HTMLProcessor,
    MarkdownProcessor,
    NotebookProcessor,
    ODTProcessor,
    PPTProcessor,
    PythonProcessor,
    TikTokenTxtProcessor,
    XLSXProcessor,
)

from .processor_base import ProcessorBase

logger = logging.getLogger("quivr_core")

_LOWEST_PRIORITY = 100

_registry: dict[str, Type[ProcessorBase]] = {}

# external, read only. Contains the actual processors that we are imported and ready to use
registry = types.MappingProxyType(_registry)


@dataclass(order=True)
class ProcEntry:
    priority: int
    cls_mod: str = field(compare=False)
    err: str | None = field(compare=False)


ProcMapping: TypeAlias = dict[FileExtension | str, list[ProcEntry]]

# Register based on mimetypes
base_processors: ProcMapping = {
    FileExtension.txt: [
        ProcEntry(
            cls_mod="quivr_core.processor.implementations.simple_txt_processor.SimpleTxtProcessor",
            err=None,
            priority=_LOWEST_PRIORITY,
        )
    ],
    FileExtension.pdf: [
        ProcEntry(
            cls_mod="quivr_core.processor.implementations.tika_processor.TikaProcessor",
            err=None,
            priority=_LOWEST_PRIORITY,
        )
    ],
}


def _append_proc_mapping(
    mapping: ProcMapping,
    file_ext: FileExtension | str,
    cls_mod: str,
    errtxt: str,
    priority: int | None,
):
    if file_ext in mapping:
        prev_proc = heappop(mapping[file_ext])
        proc_entry = ProcEntry(
            priority=priority if priority is not None else prev_proc.priority - 1,
            cls_mod=cls_mod,
            err=errtxt,
        )
        # Repush the previous processor
        heappush(mapping[file_ext], prev_proc)
        heappush(mapping[file_ext], proc_entry)
    else:
        proc_entry = ProcEntry(
            priority=priority if priority is not None else _LOWEST_PRIORITY,
            cls_mod=cls_mod,
            err=errtxt,
        )
        mapping[file_ext] = [proc_entry]


def defaults_to_proc_entries(
    base_processors: ProcMapping,
) -> ProcMapping:
    # TODO(@aminediro) : how can a user change the order of the processor ?
    # NOTE: order of this list is important as resolution of `get_processor_class` depends on it
    for processor in [
        CSVProcessor,
        TikTokenTxtProcessor,
        DOCXProcessor,
        XLSXProcessor,
        PPTProcessor,
        MarkdownProcessor,
        EpubProcessor,
        BibTexProcessor,
        ODTProcessor,
        HTMLProcessor,
        PythonProcessor,
        NotebookProcessor,
    ]:
        for ext in processor.supported_extensions:
            ext_str = ext.value if isinstance(ext, FileExtension) else ext
            _append_proc_mapping(
                mapping=base_processors,
                file_ext=ext,
                cls_mod=f"quivr_core.processor.implementations.default.{processor.__name__}",
                errtxt=f"can't import {processor.__name__}. Please install quivr-core[{ext_str}] to access {processor.__name__}",
                priority=None,
            )

    return base_processors


known_processors = defaults_to_proc_entries(base_processors)


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
        # Either you registered it from module or it's in the known processors
        if file_extension not in known_processors:
            raise ValueError(f"Extension not known: {file_extension}")
        entries = known_processors[file_extension]
        while entries:
            proc_entry = heappop(entries)
            try:
                register_processor(file_extension, _import_class(proc_entry.cls_mod))
                break
            except ImportError:
                logger.warn(
                    f"{proc_entry.err}. Falling to the next available processor for {file_extension}"
                )
        if len(entries) == 0 and file_extension not in registry:
            raise ImportError(f"can't find any processor for {file_extension}")

    cls = registry[file_extension]
    return cls


def register_processor(
    file_ext: FileExtension | str,
    proc_cls: str | Type[ProcessorBase],
    append: bool = False,
    errtxt=None,
    priority: int | None = None,
):
    if isinstance(proc_cls, str):
        if file_ext in known_processors and append is False:
            if all(proc_cls != proc.cls_mod for proc in known_processors[file_ext]):
                raise ValueError(
                    f"Processor for ({file_ext}) already in the registry and append is False"
                )
        else:
            _append_proc_mapping(
                known_processors,
                file_ext=file_ext,
                cls_mod=proc_cls,
                errtxt=errtxt
                or f"{proc_cls} import failed for processor of {file_ext}",
                priority=priority,
            )

    else:
        if file_ext in registry and append is False:
            if _registry[file_ext] is not proc_cls:
                raise ValueError(
                    f"Processor for ({file_ext}) already in the registry and append is False"
                )
        else:
            _registry[file_ext] = proc_cls


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
