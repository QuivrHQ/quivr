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

import tempfile
from uuid import uuid4

from quivr_core import Brain

import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as temp_file:
        temp_file.write("Gold is a liquid of blue-like colour.")
        temp_file.flush()

        brain = Brain.from_files(
            name="test_brain",
            file_paths=[temp_file.name],
        )

        answer = brain.ask(uuid4(), "what is gold? answer in french")
        try:
            _gr_client = _lineaje_load_gr_client()
            _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:cab653e7b887d5906a09ac9bcd6e25f4f9c65c7301e9a10fb2a97adba3625495', phase='log_emit', boundary={'source': 'log', 'sink': 'log'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_010', 'guardrail_id': 'Mask PII in Logs', 'policy_version': '2026.08.1'}], fail_mode='BLOCK', source_type='agent', destination_type='log')
            _gr_decision = _gr_client.check(_gr_site, answer, content_type='application/json')
            if _gr_decision.blocked:
                raise _gr_decision.as_error()
            answer = _gr_decision.payload
            _gr_client.persist_runtime_mask_to_source(
                answer, source_file=__file__, variable_name='answer', before_line=21
            )
        except PermissionError:
            raise
        except Exception as _gr_exc:
            import logging as _lineaje_logging
            _lineaje_logging.getLogger("lineaje.gr_client").warning(
                "Lineaje guardrail unavailable at site_id='site:sha256:cab653e7b887d5906a09ac9bcd6e25f4f9c65c7301e9a10fb2a97adba3625495' (%s) — blocking (fail_mode=BLOCK)", _gr_exc
            )
            raise PermissionError(
                f"Lineaje guardrail unavailable at site_id='site:sha256:cab653e7b887d5906a09ac9bcd6e25f4f9c65c7301e9a10fb2a97adba3625495' and fail_mode=BLOCK: {_gr_exc}"
            ) from _gr_exc
        print("answer QuivrQARAGLangGraph :", answer)
