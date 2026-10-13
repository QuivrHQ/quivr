#!/usr/bin/env python3
"""Verify or download the pinned multilingual-E5 snapshot for offline TEI."""

import argparse
import hashlib
import json
import os
import pathlib
import platform
import tempfile
import time
import urllib.parse
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL = ROOT / '.scratch/e5-model'
LOCK = json.loads((ROOT / 'third_party/e5/model-lock.json').read_text())
REPOSITORY = 'intfloat/multilingual-e5-small'
SUPPORTED = {('Linux', 'x86_64'), ('Darwin', 'arm64')}
DOWNLOAD_TIMEOUT_SECONDS = 120


def digest(path):
    with pathlib.Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def _mirror_base_url(value):
    if value is None:
        return None
    if (not isinstance(value, str) or not value
            or any(character.isspace() or ord(character) < 32 for character in value)):
        raise ValueError('model mirror must be a nonempty HTTP(S) URL')
    parsed = urllib.parse.urlsplit(value)
    if (parsed.scheme not in ('http', 'https') or not parsed.netloc
            or parsed.username is not None or parsed.password is not None
            or parsed.query or parsed.fragment):
        raise ValueError('model mirror must be an HTTP(S) URL without credentials or query')
    if '..' in pathlib.PurePosixPath(parsed.path).parts:
        raise ValueError('model mirror path must not contain parent traversal')
    return value.rstrip('/')


def _asset_path(output, name):
    root = pathlib.Path(output).resolve()
    relative = pathlib.PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise RuntimeError('invalid E5 model asset path')
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise RuntimeError('invalid E5 model asset path') from exc
    return path


def _asset_url(name, *, mirror=None):
    base = _mirror_base_url(mirror) or 'https://huggingface.co'
    return (base + '/' + urllib.parse.quote(REPOSITORY, safe='/')
            + '/resolve/' + urllib.parse.quote(LOCK['model_revision'], safe='') + '/'
            + urllib.parse.quote(name, safe='/'))


def _verify_asset(output, name, expected):
    path = _asset_path(output, name)
    if not path.is_file():
        raise RuntimeError('missing pinned model asset: ' + name)
    if digest(path) != expected:
        raise RuntimeError('Pinned model checksum mismatch: ' + name)
    return path


def verify(output=None):
    output = pathlib.Path(output or MODEL)
    for name, expected in LOCK['files'].items():
        _verify_asset(output, name, expected)
    return LOCK


def _download(output, name, expected, *, mirror=None):
    path = _asset_path(output, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix='.' + path.name + '.', suffix='.partial',
                                           dir=path.parent)
    temporary = pathlib.Path(temporary_name)
    try:
        with os.fdopen(fd, 'wb') as output_stream:
            with urllib.request.urlopen(_asset_url(name, mirror=mirror),
                                        timeout=DOWNLOAD_TIMEOUT_SECONDS) as response:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    output_stream.write(chunk)
            output_stream.flush()
            os.fsync(output_stream.fileno())
        if digest(temporary) != expected:
            raise RuntimeError('Pinned model checksum mismatch: ' + name)
        temporary.chmod(0o644)
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def prepare(output=None, *, verify_only=False, mirror=None, mirror_base_url=None):
    """Verify an existing snapshot or download missing/corrupt assets atomically.

    ``prepare()`` without arguments retains the local stack's historical output
    path and return shape. ``mirror`` is the short CLI/cache-wrapper spelling;
    ``mirror_base_url`` is accepted for parity with the Gemma preparer.
    """
    output = pathlib.Path(output or MODEL)
    if mirror is not None and mirror_base_url is not None and mirror != mirror_base_url:
        raise ValueError('mirror and mirror_base_url disagree')
    mirror = _mirror_base_url(mirror if mirror is not None else mirror_base_url)
    if (platform.system(), platform.machine()) not in SUPPORTED:
        raise RuntimeError(
            'The local stack runs on Linux x86_64 and on macOS with Apple Silicon (arm64); '
            f'this machine is {platform.system()} {platform.machine()}.'
        )
    started = time.monotonic()
    downloaded = 0
    if verify_only:
        verify(output)
    else:
        output.mkdir(parents=True, exist_ok=True)
        for name, expected in LOCK['files'].items():
            path = _asset_path(output, name)
            try:
                _verify_asset(output, name, expected)
            except RuntimeError:
                _download(output, name, expected, mirror=mirror)
                _verify_asset(output, name, expected)
                downloaded += path.stat().st_size
            else:
                path.chmod(0o644)
        verify(output)
    return {
        'model_revision': LOCK['model_revision'],
        'tei_image': LOCK['tei_image'],
        'files': LOCK['files'],
        'downloaded_bytes': downloaded,
        'prepare_seconds': round(time.monotonic() - started, 3),
        'architecture': 'linux/amd64',
        'device': 'CPU',
        'dtype': 'float32',
        'backend': 'ONNX',
    }


def _parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=pathlib.Path, default=MODEL)
    parser.add_argument('--verify-only', action='store_true')
    parser.add_argument('--mirror-base-url', '--mirror', dest='mirror_base_url')
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    result = {
        **prepare(args.output, verify_only=args.verify_only,
                  mirror_base_url=args.mirror_base_url),
        'output': str(args.output),
        'verify_only': args.verify_only,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
