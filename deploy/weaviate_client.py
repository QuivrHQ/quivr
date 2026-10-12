"""Credential-safe HTTP transport for Weaviate's JSON API."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request


class WeaviateClientError(RuntimeError):
    """A safe, bounded failure from a Weaviate HTTP request."""


def api_key_from_environment(environ=None):
    """Return the optional standalone-client key without exposing the environment."""
    values = os.environ if environ is None else environ
    value = values.get('WEAVIATE_API_KEY', '')
    return value if isinstance(value, str) else ''


def api_key_from_config(config):
    """Return the optional runtime-configured key, preserving anonymous omission."""
    value = config.get('weaviate_api_key', '') if isinstance(config, dict) else ''
    return value if isinstance(value, str) else ''


def _origin(url):
    try:
        parsed = urllib.parse.urlsplit(url)
        port = parsed.port
    except (TypeError, ValueError):
        raise WeaviateClientError('Weaviate URL is invalid') from None
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise WeaviateClientError('Weaviate URL is invalid')
    return parsed.scheme, parsed.hostname.lower(), port or (443 if parsed.scheme == 'https' else 80)


class _OriginRestrictedRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, origin):
        self.origin = origin

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if _origin(newurl) != self.origin:
            raise WeaviateClientError('Weaviate redirect refused') from None
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected is not None and req.has_header('Authorization'):
            redirected.add_unredirected_header('Authorization', req.get_header('Authorization'))
        return redirected


class WeaviateClient:
    """A small JSON client with an optional bearer credential and safe failures."""

    def __init__(self, base_url, api_key='', trust_env=True):
        self.base_url = base_url.rstrip('/')
        self.origin = _origin(self.base_url)
        if not isinstance(api_key, str):
            api_key = ''
        if any(character in api_key for character in '\r\n'):
            raise WeaviateClientError('Weaviate API key is invalid')
        self.api_key = api_key
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler(None if trust_env else {}), _OriginRestrictedRedirect(self.origin))

    @classmethod
    def from_config(cls, config):
        return cls(config['weaviate_url'], api_key_from_config(config))

    @classmethod
    def from_environment(cls, base_url):
        return cls(base_url, api_key_from_environment())

    def request(self, path, method='GET', body=None, timeout=10, max_bytes=8 << 20):
        url = self.base_url + '/' + path.lstrip('/')
        payload = body if isinstance(body, bytes) else (
            None if body is None else json.dumps(body, separators=(',', ':')).encode())
        headers = {}
        if payload is not None:
            headers['Content-Type'] = 'application/json'
        if self.api_key:
            headers['Authorization'] = 'Bearer ' + self.api_key
        request = urllib.request.Request(url, data=payload, method=method, headers=headers)
        try:
            with self.opener.open(request, timeout=timeout) as response:
                raw = response.read(max_bytes + 1)
                if len(raw) > max_bytes:
                    raise WeaviateClientError('Weaviate response exceeded the size limit') from None
                return response.status, raw
        except WeaviateClientError:
            raise
        except urllib.error.HTTPError as error:
            raise WeaviateClientError('Weaviate HTTP request failed (' + str(error.code) + ')') from None
        except Exception:
            raise WeaviateClientError('Weaviate transport request failed') from None

    def request_json(self, path, method='GET', body=None, timeout=10, max_bytes=8 << 20):
        _, raw = self.request(path, method=method, body=body, timeout=timeout, max_bytes=max_bytes)
        if not raw:
            return None
        try:
            return json.loads(raw)
        except (TypeError, ValueError):
            raise WeaviateClientError('Weaviate response was not valid JSON') from None
