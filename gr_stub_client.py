"""Stdlib HTTP client for GR /enforce. Copied into the scanned repo at runtime.

``check(site, payload)`` is the current stub API. ``call_gr_enforce`` remains
for older inserted sites. Both fail open unless the site fail_mode is BLOCK.
"""
from __future__ import annotations

import json
import logging
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any

_logger = logging.getLogger("aipo_mcp.gr_stub_client")

_RUNTIME_ENV_LOADED = False
_MANIFEST_CACHE: dict[str, Any] | None = None
_ACCESS_TOKEN_CACHE: dict[str, tuple[str, float]] = {}
_TOKEN_LOCK = threading.Lock()
_TOKEN_SKEW_SEC = 120


def _reset_runtime_caches() -> None:
    """Test helper — drop manifest / access-token caches."""
    global _RUNTIME_ENV_LOADED, _MANIFEST_CACHE
    _RUNTIME_ENV_LOADED = False
    _MANIFEST_CACHE = None
    _ACCESS_TOKEN_CACHE.clear()


def _guardrail_manifest_candidates() -> list[str]:
    here = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()
    candidates = [
        os.path.join(here, ".lineaje", "guardrail.json"),
        os.path.join(cwd, ".lineaje", "guardrail.json"),
    ]
    # Walk parents so a nested source file can still find repo-root manifest.
    cur = here
    for _ in range(6):
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        candidates.append(os.path.join(parent, ".lineaje", "guardrail.json"))
        cur = parent
    return candidates


def _load_guardrail_manifest() -> dict[str, Any]:
    """Load ``.lineaje/guardrail.json`` (written by GHA PRs / MCP workflow)."""
    global _MANIFEST_CACHE
    if _MANIFEST_CACHE is not None:
        return _MANIFEST_CACHE
    for path in _guardrail_manifest_candidates():
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                _MANIFEST_CACHE = data
                return data
        except (OSError, ValueError, TypeError):
            continue
    _MANIFEST_CACHE = {}
    return _MANIFEST_CACHE


def _load_guardrail_manifest_url() -> str:
    """Enforce URL from ``.lineaje/guardrail.json``."""
    return (_load_guardrail_manifest().get("gr_service_url") or "").strip().rstrip("/")


def _looks_like_jwt(value: str) -> bool:
    s = (value or "").strip()
    return s.count(".") == 2 and s.startswith("eyJ")


def _parse_access_token(raw_text: str) -> str:
    text = (raw_text or "").strip()
    if not text:
        return ""
    try:
        parsed: Any = json.loads(text)
    except json.JSONDecodeError:
        return text if _looks_like_jwt(text) else ""
    if isinstance(parsed, str):
        return parsed.strip()
    if isinstance(parsed, dict):
        return (parsed.get("access_token") or "").strip()
    return ""


def _jwt_exp_epoch(token: str) -> float:
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        import base64
        data = json.loads(base64.urlsafe_b64decode(payload))
        exp = data.get("exp")
        if isinstance(exp, (int, float)):
            return float(exp)
    except Exception:
        pass
    return time.time() + 3600.0


def _exchange_refresh_for_access(refresh_token: str, renew_url: str) -> str:
    """POST renew-access-token?refreshToken=… → short-lived access JWT. Empty on failure."""
    if not refresh_token or not renew_url:
        return ""
    key = refresh_token
    now = time.time()
    cached = _ACCESS_TOKEN_CACHE.get(key)
    if cached is not None:
        access, deadline = cached
        if access and now < deadline - _TOKEN_SKEW_SEC:
            return access
    q = urllib.parse.urlencode({"refreshToken": refresh_token})
    req = urllib.request.Request(
        f"{renew_url.rstrip('/')}?{q}",
        data=b"null",
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            access = _parse_access_token(resp.read().decode())
    except Exception as exc:
        _logger.warning("refresh-token exchange failed (%s) — using refresh token as Bearer", exc)
        return ""
    if not access:
        return ""
    _ACCESS_TOKEN_CACHE[key] = (access, _jwt_exp_epoch(access))
    return access


def _resolve_enforce_bearer(lineaje_pat: str = "") -> str:
    """Return the Authorization Bearer for POST /enforce.

    Prefer an already-usable JWT. Otherwise take ``refreshtoken`` from
    ``.lineaje/guardrail.json`` (or LINEAJE_REFRESH_TOKEN / LINEAJE_PAT_TOKEN),
    exchange it at renew-access-token, and use the minted access token.
    If the exchange is unconfigured or fails, send the refresh token itself —
    /enforce can exchange it server-side.
    """
    explicit = (lineaje_pat or os.environ.get("GR_BEARER_TOKEN") or "").strip()
    if explicit and _looks_like_jwt(explicit):
        return explicit

    env_pat = (
        os.environ.get("LINEAJE_PAT_TOKEN")
        or os.environ.get("LINEAJE_PAT")
        or ""
    ).strip()
    if env_pat and _looks_like_jwt(env_pat):
        return env_pat

    manifest = _load_guardrail_manifest()
    refresh = (
        os.environ.get("LINEAJE_REFRESH_TOKEN")
        or (explicit if explicit and not _looks_like_jwt(explicit) else "")
        or (env_pat if env_pat and not _looks_like_jwt(env_pat) else "")
        or (manifest.get("refreshtoken") or manifest.get("refresh_token") or "")
    ).strip()
    if not refresh:
        return explicit or env_pat

    if _looks_like_jwt(refresh):
        return refresh

    renew_url = (
        (os.environ.get("LINEAJE_RENEW_ACCESS_TOKEN_URL") or "").strip()
        or (manifest.get("renew_access_token_url") or "").strip()
    )
    with _TOKEN_LOCK:
        access = _exchange_refresh_for_access(refresh, renew_url)
    return access or refresh


def _ensure_runtime_env_loaded() -> None:
    """Load GR_SERVICE_URL / PAT from a nearby .env or .lineaje/guardrail.json."""
    global _RUNTIME_ENV_LOADED
    if _RUNTIME_ENV_LOADED:
        return
    _RUNTIME_ENV_LOADED = True
    _keys = frozenset({
        "GR_SERVICE_URL", "LINEAJE_PAT_TOKEN", "LINEAJE_PAT", "GR_BEARER_TOKEN",
        "LINEAJE_REFRESH_TOKEN", "LINEAJE_RENEW_ACCESS_TOKEN_URL",
    })
    _candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        os.path.join(os.getcwd(), ".env"),
    ]
    for path in _candidates:
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#") or "=" not in stripped:
                        continue
                    key, _, val = stripped.partition("=")
                    key = key.strip()
                    if key in _keys and key not in os.environ:
                        os.environ[key] = val.strip().strip('"').strip("'")
        except OSError:
            pass
        break
    if not os.environ.get("GR_SERVICE_URL"):
        manifest_url = _load_guardrail_manifest_url()
        if manifest_url:
            os.environ["GR_SERVICE_URL"] = manifest_url


def call_gr_enforce(
    data: Any,
    source_type: str,
    destination_type: str,
    lineaje_pat: str = "",
    gr_service_url: str | None = None,
    violations: list[dict] | None = None,
    enabled_policies: list[str] | None = None,
    candidate_policies: list[str] | None = None,
    site_id: str | None = None,
    tenant_id: str = "",
    timeout: float = 5.0,
) -> dict[str, Any]:
    """POST /enforce. Fail-open on errors; 403 is a real block."""
    _ensure_runtime_env_loaded()
    url = (gr_service_url or os.environ.get("GR_SERVICE_URL") or "").rstrip("/")
    if not url:
        return {
            "status": "allow",
            "result": {"data": data},
            "actions_applied": [],
            "recommendations": [],
            "warning": "GR_SERVICE_URL not configured — guardrail skipped (fail-open)",
        }

    pat = _resolve_enforce_bearer(lineaje_pat)
    params_key = "out_params" if destination_type == "agent" else "in_params"

    body: dict[str, Any] = {
        "source_type": source_type,
        "destination_type": destination_type,
        params_key: {"data": _jsonable_payload(data)},
    }
    if violations:
        body["violations"] = violations
    if enabled_policies:
        body["enabled_policies"] = enabled_policies
    if candidate_policies:
        body["candidate_policies"] = candidate_policies
    if site_id:
        body["site_id"] = site_id
    if tenant_id:
        body["tenant_id"] = tenant_id

    req = urllib.request.Request(
        f"{url}/enforce",
        data=json.dumps(body, default=_json_default).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {pat}",
        },
        method="POST",
    )

    hop = f"{source_type}->{destination_type}"
    if site_id:
        hop = f"{hop} site_id={site_id}"
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read())
        if result.get("status") == "escalate":
            _logger.warning("gr_stub_client[%s]: escalation flagged — passing through for human review", hop)
        return result
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            try:
                detail = json.loads(exc.read()).get("detail", {})
            except Exception:
                detail = {}
            blocked_by = detail.get("blocked_by") or []
            policy_id = blocked_by[0].get("policy_id", "unknown") if blocked_by else "unknown"
            reason = detail.get("message", "Request denied by policy enforcement.")
            _logger.warning("gr_stub_client[%s]: BLOCKED by policy=%s — %s", hop, policy_id, reason)
            return {
                "status": "block",
                "result": {"data": data},
                "actions_applied": [{"policy_id": policy_id, "action": "block"}],
                "recommendations": [],
                "warning": reason,
            }
        _logger.warning("gr_stub_client[%s]: GR service call failed (%s) — failing open", hop, exc)
        return {
            "status": "allow",
            "result": {"data": data},
            "actions_applied": [],
            "recommendations": [],
            "warning": f"GR service error: {exc}",
        }
    except Exception as exc:
        _logger.warning("gr_stub_client[%s]: GR service call failed (%s) — failing open", hop, exc)
        return {
            "status": "allow",
            "result": {"data": data},
            "actions_applied": [],
            "recommendations": [],
            "warning": f"GR service unreachable: {exc}",
        }



_CROCKFORD_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _new_ulid() -> str:
    """26-char Crockford ULID (48-bit timestamp + 80-bit randomness)."""
    import os as _os
    import time as _time

    ts_ms = int(_time.time() * 1000) & 0xFFFFFFFFFFFF  # 48 bits
    rand = int.from_bytes(_os.urandom(10), "big")  # 80 bits
    value = (ts_ms << 80) | rand
    chars = []
    for _ in range(26):
        chars.append(_CROCKFORD_ALPHABET[value & 0x1F])
        value >>= 5
    return "".join(reversed(chars))


@dataclass
class SiteDescriptor:
    """Scan-time facts for one call site. ``fail_mode`` is ALLOW_WITH_AUDIT or BLOCK."""
    site_id: str
    phase: str = ""
    boundary: dict = field(default_factory=dict)
    components: dict = field(default_factory=dict)
    candidate_policies: "list[dict]" = field(default_factory=list)
    site_manifest_version: "str | None" = None
    fail_mode: str = "ALLOW_WITH_AUDIT"
    source_type: str = ""
    destination_type: str = ""


_PHASE_BOUNDARY_TO_SOURCE_DEST: dict[tuple[str, str, str], tuple[str, str]] = {
    ("pre_model", "agent_message", "model"): ("agent", "llm"),
    ("pre_model", "user_interface", "model"): ("user_interface", "llm"),
    ("post_model", "model", "agent_message"): ("llm", "agent"),
    ("pre_agent_send", "agent_message", "agent_message"): ("agent", "agent"),
    ("post_agent_receive", "user_interface", "agent_message"): ("user_interface", "agent"),
    ("post_tool", "database", "agent_message"): ("database", "agent"),
    ("post_tool", "external_endpoint", "agent_message"): ("api", "agent"),
    ("post_tool", "tool_result", "agent_message"): ("agent", "tool"),
    ("pre_tool", "agent_message", "tool_result"): ("agent", "tool"),
    ("pre_tool", "user_interface", "tool_result"): ("user_interface", "tool"),
    ("data_egress", "model", "user_interface"): ("llm", "user_interface"),
    ("data_egress", "agent_message", "user_interface"): ("agent", "user_interface"),
    ("data_egress", "agent_message", "external_endpoint"): ("agent", "external"),
    ("data_egress", "tool_result", "user_interface"): ("tool", "user_interface"),
    ("data_egress", "html", "user_interface"): ("html", "user_interface"),
    ("security_decision", "agent_message", "agent_message"): ("agent", "policy_engine"),
    ("log_emit", "log", "log"): ("agent", "log"),
}


def _source_dest_from_site(site: "SiteDescriptor") -> tuple[str, str]:
    src = getattr(site, "source_type", "") or ""
    dst = getattr(site, "destination_type", "") or ""
    if src and dst:
        return src, dst
    boundary = getattr(site, "boundary", None) or {}
    return _PHASE_BOUNDARY_TO_SOURCE_DEST.get(
        (getattr(site, "phase", "") or "", boundary.get("source") or "", boundary.get("sink") or ""),
        ("", ""),
    )


class Decision:
    """Result of ``check()``. Use ``blocked`` / ``payload`` / ``as_error()``."""

    def __init__(self, raw: dict, *, site_id: str = ""):
        self.raw = raw
        self.site_id = site_id
        self.status = raw.get("status", "allow")
        self.verdict = raw.get("verdict") or self.status.upper()
        self.result = raw.get("result") or {}
        self.payload = self.result.get("data")
        self.actions_applied = raw.get("actions_applied", [])
        self.recommendations = raw.get("recommendations", [])
        self.warning = raw.get("warning")

    @property
    def blocked(self) -> bool:
        return self.status == "block"

    def as_error(self) -> PermissionError:
        """PermissionError for a policy block. ``check()`` never raises this itself."""
        site_note = f" at site {self.site_id}" if self.site_id else ""
        return PermissionError(self.warning or f"blocked by guardrail policy{site_note}")


def _fail_response(site: "SiteDescriptor", warning: str, payload: Any) -> dict:
    """Unreachable GR: BLOCK sites fail closed; others fail open."""
    if getattr(site, "fail_mode", None) == "BLOCK":
        return {
            "status": "block",
            "result": {"data": payload},
            "actions_applied": [],
            "recommendations": [],
            "warning": f"{warning} — failing CLOSED (site fail_mode=BLOCK)",
        }
    return {
        "status": "allow",
        "result": {"data": payload},
        "actions_applied": [],
        "recommendations": [],
        "warning": warning,
    }


def _find_assignment_line(lines: list[str], var_name: str, before_line: int) -> int | None:
    """1-based line of ``var_name = ...`` assignment strictly before ``before_line``."""
    pat = re.compile(
        rf"^\s*(?:[A-Za-z_][\w.<>\[\],\s]*\s+)?{re.escape(var_name)}\s*(?::=|=)(?!=)\s*(?:f|[(\"']|\"\"\"|''')"
    )
    upper = min(max(before_line - 1, 0), len(lines))
    for i in range(upper - 1, -1, -1):
        if pat.match(lines[i]):
            return i + 1
    return None


def _assignment_stmt_span(lines: list[str], assign_line: int) -> tuple[int, int] | None:
    """0-based inclusive (start, end) line indices for a multi-line assignment."""
    import ast as _ast

    start = assign_line - 1
    if start < 0 or start >= len(lines):
        return None
    for end in range(start, min(start + 60, len(lines))):
        block = "".join(lines[start : end + 1])
        try:
            mod = _ast.parse(f"def __lineaje_fn():\n{block}\n")
        except SyntaxError:
            continue
        body = mod.body[0].body  # type: ignore[attr-defined]
        if not body or not isinstance(body[0], _ast.Assign):
            continue
        stmt = body[0]
        stmt_end = getattr(stmt, "end_lineno", None)
        if stmt_end is None:
            return start, end
        end_idx = start + max(0, stmt_end - 2)
        return start, min(end_idx, len(lines) - 1)
    return None


def _decode_body(raw: Any) -> Any:
    """Bytes/str body → parsed JSON if possible, else unicode text."""
    if raw is None:
        return None
    if isinstance(raw, (bytes, bytearray)):
        text = bytes(raw).decode("utf-8", errors="replace")
        try:
            return json.loads(text)
        except ValueError:
            return text
    return raw


def _document_like(obj: Any) -> bool:
    """LangChain Document (and lookalikes) carry text on ``page_content``."""
    return isinstance(getattr(obj, "page_content", None), str)


def _pydantic_dump(obj: Any) -> "dict | None":
    if not (hasattr(obj, "model_fields") or hasattr(obj, "__fields__")):
        return None
    dump = getattr(obj, "model_dump", None) or getattr(obj, "dict", None)
    if not callable(dump):
        return None
    try:
        data = dump()
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _jsonable_payload(payload: Any) -> Any:
    """JSON-serializable form of payload (unwrap Request / Document objects)."""
    if payload is None or isinstance(payload, (str, int, float, bool)):
        return payload
    if isinstance(payload, dict):
        return {str(k): _jsonable_payload(v) for k, v in payload.items()}
    if isinstance(payload, (list, tuple)):
        return [_jsonable_payload(item) for item in payload]
    if isinstance(payload, (bytes, bytearray)):
        return _decode_body(payload)
    data = getattr(payload, "data", None)
    if isinstance(payload, urllib.request.Request) or (
        type(payload).__name__ == "Request" and data is not None
    ):
        return _decode_body(data)
    if _document_like(payload):
        meta = getattr(payload, "metadata", None)
        out: dict[str, Any] = {"page_content": payload.page_content}
        if isinstance(meta, dict):
            out["metadata"] = _jsonable_payload(meta)
        return out
    dumped = _pydantic_dump(payload)
    if dumped is not None:
        return _jsonable_payload(dumped)
    return payload


def _json_default(obj: Any) -> Any:
    """json.dumps default: coerce leftover objects instead of failing open."""
    coerced = _jsonable_payload(obj)
    if coerced is not obj:
        return coerced
    return str(obj)


def _looks_like_object_repr(text: str) -> bool:
    """True for ``str(Document)`` / ``str(obj)`` dumps, not real masked text."""
    if text.startswith("page_content=") or "page_content=" in text[:80]:
        return True
    if text.startswith("<") and "object at 0x" in text:
        return True
    return False


def _rehydrate_item(original: Any, masked: Any) -> Any:
    """Write masked fields onto the original object when possible."""
    if original is None:
        return masked
    if isinstance(original, urllib.request.Request):
        return _reapply_payload(original, masked)
    if _document_like(original):
        if isinstance(masked, dict) and "page_content" in masked:
            original.page_content = masked["page_content"]
            if isinstance(masked.get("metadata"), dict) and hasattr(original, "metadata"):
                original.metadata = masked["metadata"]
            return original
        if isinstance(masked, str) and not _looks_like_object_repr(masked):
            original.page_content = masked
            return original
        return original
    if type(masked) is type(original):
        return masked
    if not isinstance(original, (str, int, float, bool, dict, list, type(None))):
        return original
    return masked


def _reapply_payload(original: Any, masked: Any) -> Any:
    """Put masked data back on the live object; keep the original type."""
    if isinstance(original, urllib.request.Request):
        if isinstance(masked, (dict, list)):
            original.data = json.dumps(masked).encode("utf-8")
        elif isinstance(masked, str):
            original.data = masked.encode("utf-8")
        elif isinstance(masked, (bytes, bytearray)):
            original.data = bytes(masked)
        return original
    if isinstance(original, (list, tuple)) and isinstance(masked, list):
        rehydrated = [
            _rehydrate_item(item, masked[i] if i < len(masked) else item)
            for i, item in enumerate(original)
        ]
        return type(original)(rehydrated) if isinstance(original, tuple) else rehydrated
    return _rehydrate_item(original, masked)


def persist_runtime_mask_to_source(
    masked_payload: Any,
    *,
    source_file: str,
    variable_name: str,
    before_line: int | None = None,
) -> bool:
    """Replace a source literal assignment with the masked value. Scalars only."""
    if not isinstance(masked_payload, (str, int, float, bool)):
        return False
    masked_text = str(masked_payload)
    path = os.path.abspath(source_file)
    if not os.path.isfile(path):
        _logger.warning("persist_runtime_mask_to_source: missing file %s", path)
        return False
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as exc:
        _logger.warning("persist_runtime_mask_to_source: read failed %s (%s)", path, exc)
        return False

    assign_line = _find_assignment_line(lines, variable_name, before_line or len(lines))
    if assign_line is None:
        _logger.debug(
            "persist_runtime_mask_to_source: no assignment for %r before line %s in %s",
            variable_name, before_line, path,
        )
        return False
    span = _assignment_stmt_span(lines, assign_line)
    if span is None:
        _logger.warning(
            "persist_runtime_mask_to_source: could not span assignment for %r at line %d in %s",
            variable_name, assign_line, path,
        )
        return False
    start, end = span
    original = "".join(lines[start : end + 1])
    if "_gr_client" in original or "SiteDescriptor" in original:
        _logger.debug(
            "persist_runtime_mask_to_source: skip guardrail stub assignment %r in %s",
            variable_name, path,
        )
        return False
    if re.search(r"""=\s*(?:\()?\s*f(?:'''|\"\"\"|'|\")""", original) or re.search(
        r"\bf(?:'''|\"\"\"|'|\")", original
    ):
        _logger.info(
            "persist_runtime_mask_to_source: skip f-string assignment %r in %s",
            variable_name, path,
        )
        return False
    indent_match = re.match(r"^(\s*)", lines[start])
    base_indent = indent_match.group(1) if indent_match else ""
    quote = "'''" if '"""' in masked_text else '"""'
    new_lines = [f"{base_indent}{variable_name} = {quote}{masked_text}{quote}\n"]
    rewritten = lines[:]
    rewritten[start : end + 1] = new_lines
    try:
        compile("".join(rewritten), path, "exec")
    except SyntaxError as exc:
        _logger.warning(
            "persist_runtime_mask_to_source: rewrite would be invalid Python (%s) — left %s unchanged",
            exc, path,
        )
        return False
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.writelines(rewritten)
    except OSError as exc:
        _logger.warning("persist_runtime_mask_to_source: write failed %s (%s)", path, exc)
        return False
    _logger.info(
        "persist_runtime_mask_to_source: updated %s lines %d-%d (%r)",
        path, start + 1, end + 1, variable_name,
    )
    return True


def check(
    site: SiteDescriptor,
    payload: Any,
    content_type: str = "application/json",
    *,
    tenant_id: str = "",
    correlation_id: "str | None" = None,
    event_id: "str | None" = None,
    operation_identity: "dict | None" = None,
    gr_service_url: "str | None" = None,
    lineaje_pat: str = "",
    timeout: float = 5.0,
) -> Decision:
    """POST /enforce for this site. Never raises; 403 → ``decision.blocked``."""
    _ensure_runtime_env_loaded()
    url = (gr_service_url or os.environ.get("GR_SERVICE_URL") or "").rstrip("/")
    if not url:
        return Decision(
            _fail_response(site, "GR_SERVICE_URL not configured — guardrail skipped", payload),
            site_id=site.site_id,
        )

    pat = _resolve_enforce_bearer(lineaje_pat)

    wire_src, wire_dst = _source_dest_from_site(site)
    body: dict[str, Any] = {
        "contract_version": "2.0",
        "event_id": event_id or _new_ulid(),
        "correlation_id": correlation_id or _new_ulid(),
        "tenant_id": tenant_id or os.environ.get("GR_TENANT_ID", ""),
        "site_id": site.site_id,
        "site_manifest_version": site.site_manifest_version,
        "phase": site.phase,
        "candidate_policies": site.candidate_policies,
        "boundary": site.boundary,
        "components": site.components,
        "source_type": wire_src,
        "destination_type": wire_dst,
        "payload": {"mode": "inline", "content_type": content_type, "data": _jsonable_payload(payload)},
        "client_deadline_hint_ms": int(timeout * 1000),
        "resume_token": None,
        "redecision_token": None,
        "operation_identity": operation_identity,
    }

    req = urllib.request.Request(
        f"{url}/enforce",
        data=json.dumps(body, default=_json_default).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {pat}",
        },
        method="POST",
    )

    hop = f"site_id={site.site_id}" if site.site_id else "site_id=<unknown>"
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read())
        if result.get("status") == "escalate":
            _logger.warning("gr_stub_client.check[%s]: escalation flagged — passing through for human review", hop)
        server_result = result.get("result")
        wire_payload = _jsonable_payload(payload)
        if not isinstance(wire_payload, dict) and isinstance(server_result, dict) and "text" in server_result:
            result["result"] = {"data": server_result["text"]}
        else:
            result["result"] = {"data": server_result}
        decision = Decision(result, site_id=site.site_id)
        decision.payload = _reapply_payload(payload, decision.payload)
        return decision
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            try:
                detail = json.loads(exc.read()).get("detail", {})
            except Exception:
                detail = {}
            blocked_by = detail.get("blocked_by") or []
            policy_id = blocked_by[0].get("policy_id", "unknown") if blocked_by else "unknown"
            reason = detail.get("message", "Request denied by policy enforcement.")
            _logger.warning("gr_stub_client.check[%s]: BLOCKED by policy=%s — %s", hop, policy_id, reason)
            return Decision({
                "status": "block",
                "result": {"data": payload},
                "actions_applied": [{"policy_id": policy_id, "action": "block"}],
                "recommendations": [],
                "warning": reason,
            }, site_id=site.site_id)
        _logger.warning(
            "gr_stub_client.check[%s]: GR service call failed (%s) — %s", hop, exc,
            "failing closed (fail_mode=BLOCK)" if site.fail_mode == "BLOCK" else "failing open",
        )
        return Decision(_fail_response(site, f"GR service error: {exc}", payload), site_id=site.site_id)
    except Exception as exc:
        _logger.warning(
            "gr_stub_client.check[%s]: GR service call failed (%s) — %s", hop, exc,
            "failing closed (fail_mode=BLOCK)" if site.fail_mode == "BLOCK" else "failing open",
        )
        return Decision(_fail_response(site, f"GR service unreachable: {exc}", payload), site_id=site.site_id)
