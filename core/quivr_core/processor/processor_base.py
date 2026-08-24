def _lineaje_load_gr_client():
    import sys as _lineaje_sys, os as _lineaje_os, importlib.util as _lineaje_ilu
    if "_lineaje_gr_stub_client" in _lineaje_sys.modules:
        return _lineaje_sys.modules["_lineaje_gr_stub_client"]
    _here = _lineaje_os.path.dirname(_lineaje_os.path.abspath(__file__))
    _cur, _path = _here, _lineaje_os.path.join(_here, "gr_stub_client.py")
    for _ in range(8):
        _cand = _lineaje_os.path.join(_cur, "gr_stub_client.py")
        if _lineaje_os.path.isfile(_cand):
            _path = _cand
            break
        _parent = _lineaje_os.path.dirname(_cur)
        if _parent == _cur:
            break
        _cur = _parent
    _spec = _lineaje_ilu.spec_from_file_location("_lineaje_gr_stub_client", _path)
    _mod = _lineaje_ilu.module_from_spec(_spec)
    _lineaje_sys.modules["_lineaje_gr_stub_client"] = _mod
    _spec.loader.exec_module(_mod)
    return _mod

import logging
from abc import ABC, abstractmethod
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Generic, List, TypeVar

from attr import dataclass
from langchain_core.documents import Document

from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.language.utils import detect_language

logger = logging.getLogger("quivr_core")


R = TypeVar("R", covariant=True)


@dataclass
class ProcessedDocument(Generic[R]):
    chunks: List[Document]
    processor_cls: str
    processor_response: R


# TODO: processors should be cached somewhere ?
# The processor should be cached by processor type
# The cache should use a single
class ProcessorBase(ABC, Generic[R]):
    supported_extensions: list[FileExtension | str]

    def check_supported(self, file: QuivrFile) -> None:
        if file.file_extension not in self.supported_extensions:
            raise ValueError(f"can't process a file of type {file.file_extension}")

    @property
    @abstractmethod
    def processor_metadata(self) -> dict[str, Any]:
        raise NotImplementedError

    async def process_file(self, file: QuivrFile) -> ProcessedDocument[R]:
        _lineaje_payload = f"Processing file {file}"
        try:
            _gr_client = _lineaje_load_gr_client()
            _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:8b74c8b50692a02c7980bd108bbeab948e28fa6426968c54f77324f72d05489f', phase='log_emit', boundary={'source': 'log', 'sink': 'log'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_010', 'guardrail_id': 'Mask PII in Logs', 'policy_version': '2026.08.1'}], fail_mode='BLOCK', source_type='agent', destination_type='log')
            import asyncio as _gr_asyncio
            _gr_decision = await _gr_asyncio.to_thread(lambda: _gr_client.check(_gr_site, _lineaje_payload, content_type='application/json'))
            if _gr_decision.blocked:
                raise _gr_decision.as_error()
            _lineaje_payload = _gr_decision.payload
            _gr_client.persist_runtime_mask_to_source(
                _lineaje_payload, source_file=__file__, variable_name='_lineaje_payload', before_line=41
            )
        except PermissionError:
            raise
        except Exception as _gr_exc:
            import logging as _lineaje_logging
            _lineaje_logging.getLogger("lineaje.gr_client").warning(
                "Lineaje guardrail unavailable at site_id='site:sha256:8b74c8b50692a02c7980bd108bbeab948e28fa6426968c54f77324f72d05489f' (%s) — blocking (fail_mode=BLOCK)", _gr_exc
            )
            raise PermissionError(
                f"Lineaje guardrail unavailable at site_id='site:sha256:8b74c8b50692a02c7980bd108bbeab948e28fa6426968c54f77324f72d05489f' and fail_mode=BLOCK: {_gr_exc}"
            ) from _gr_exc
        logger.debug(_lineaje_payload)
        self.check_supported(file)
        docs = await self.process_file_inner(file)
        try:
            qvr_version = version("quivr-core")
        except PackageNotFoundError:
            qvr_version = "dev"

        for idx, doc in enumerate(docs.chunks, start=1):
            if "original_file_name" in doc.metadata:
                doc.page_content = f"Filename: {doc.metadata['original_file_name']} Content: {doc.page_content}"
            doc.page_content = doc.page_content.replace("\u0000", "")
            doc.page_content = doc.page_content.encode("utf-8", "replace").decode(
                "utf-8"
            )
            doc.metadata = {
                "chunk_index": idx,
                "quivr_core_version": qvr_version,
                "language": detect_language(
                    text=doc.page_content.replace("\\n", " ").replace("\n", " "),
                    low_memory=True,
                ).value,
                **file.metadata,
                **doc.metadata,
                **self.processor_metadata,
            }
        try:
            _gr_client = _lineaje_load_gr_client()
            _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:309ff589e93aa7b43f80a42c5dbea3abd3bdbeceec1908c295eb6917739fc7e3', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'user_interface'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_012', 'guardrail_id': 'Mask PII on UI', 'policy_version': '2026.08.1'}], fail_mode='BLOCK', source_type='agent', destination_type='user_interface')
            _gr_decision = _gr_client.check(_gr_site, docs, content_type='text/plain')
            if _gr_decision.blocked:
                raise _gr_decision.as_error()
            docs = _gr_decision.payload
        except PermissionError:
            raise
        except Exception as _gr_exc:
            import logging as _lineaje_logging
            _lineaje_logging.getLogger("lineaje.gr_client").warning(
                "Lineaje guardrail unavailable at site_id='site:sha256:309ff589e93aa7b43f80a42c5dbea3abd3bdbeceec1908c295eb6917739fc7e3' (%s) — blocking (fail_mode=BLOCK)", _gr_exc
            )
            raise PermissionError(
                f"Lineaje guardrail unavailable at site_id='site:sha256:309ff589e93aa7b43f80a42c5dbea3abd3bdbeceec1908c295eb6917739fc7e3' and fail_mode=BLOCK: {_gr_exc}"
            ) from _gr_exc
        return docs

    @abstractmethod
    async def process_file_inner(self, file: QuivrFile) -> ProcessedDocument[R]:
        raise NotImplementedError
