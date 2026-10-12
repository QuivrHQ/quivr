"""Credential-safe HTTP transport for Weaviate tooling."""
import json
import os
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import sys
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from deploy.weaviate_client import WeaviateClient, WeaviateClientError


class _Requests:
    def __init__(self):
        self.items = []
        self.redirect_target = None


def _handler(requests):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.items.append((self.path, self.headers.get('Authorization')))
            if self.path == '/same-redirect':
                self.send_response(302)
                self.send_header('Location', '/objects')
                self.end_headers()
                return
            if self.path == '/redirect':
                self.send_response(302)
                self.send_header('Location', requests.redirect_target)
                self.end_headers()
                return
            if self.path == '/failure':
                body = b'provider rejected Authorization: Bearer sentinel-weaviate-key'
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            body = json.dumps({'objects': []}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_):
            pass

    return Handler


class WeaviateClientTest(unittest.TestCase):
    def setUp(self):
        self.servers = []
        self.threads = []
        self.requests = []

    def tearDown(self):
        for server in self.servers:
            server.shutdown()
            server.server_close()
        for thread in self.threads:
            thread.join()

    def server(self):
        requests = _Requests()
        server = HTTPServer(('127.0.0.1', 0), _handler(requests))
        thread = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.01})
        thread.start()
        self.servers.append(server)
        self.threads.append(thread)
        self.requests.append(requests)
        return server, requests

    def test_optional_auth_redirect_and_error_safety(self):
        server, requests = self.server()
        base = f'http://127.0.0.1:{server.server_port}'
        for key, expected in (('sentinel-weaviate-key', 'Bearer sentinel-weaviate-key'), ('', None)):
            with self.subTest(key_present=bool(key)):
                config = {'weaviate_url': base}
                if key:
                    config['weaviate_api_key'] = key
                self.assertEqual(WeaviateClient.from_config(config).request_json('/objects'), {'objects': []})
                self.assertEqual(requests.items[-1][1], expected)

        # Existing tooling honors explicitly configured environment proxies.
        with patch.dict(os.environ, {'http_proxy': base, 'no_proxy': ''}, clear=True):
            self.assertEqual(WeaviateClient('http://index.example', 'sentinel-weaviate-key').request_json('/objects', timeout=1), {'objects': []})
            self.assertEqual(requests.items[-1], ('http://index.example/objects', 'Bearer sentinel-weaviate-key'))

        with self.assertRaises(WeaviateClientError) as failure:
            WeaviateClient(base, 'sentinel-weaviate-key').request_json('/failure')
        self.assertNotIn('sentinel-weaviate-key', str(failure.exception))
        self.assertIsNone(failure.exception.__cause__)

        self.assertEqual(WeaviateClient(base, 'sentinel-weaviate-key').request_json('/same-redirect'), {'objects': []})
        self.assertEqual(requests.items[-1][1], 'Bearer sentinel-weaviate-key')

        other, other_requests = self.server()
        requests.redirect_target = f'http://127.0.0.1:{other.server_port}/objects'
        with self.assertRaises(WeaviateClientError) as redirect:
            WeaviateClient(base, 'sentinel-weaviate-key').request_json('/redirect')
        self.assertIn('redirect', str(redirect.exception))
        self.assertNotIn('sentinel-weaviate-key', str(redirect.exception))
        self.assertEqual(other_requests.items, [])


if __name__ == '__main__':
    unittest.main()
