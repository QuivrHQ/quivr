#!/usr/bin/env python3
"""Prepare a verified cache; preserve the model identity of an installation."""
import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import prepare_embeddings
import prepare_query_encoder


def prepare(output, model, source=None, mirror=None, verify_only=False):
    marker = output / 'installation-model.json'
    if marker.exists() and json.loads(marker.read_text()).get('model') != model:
        raise ValueError('installation model cannot change')
    if verify_only and not marker.is_file():
        raise ValueError('model cache is not initialized')
    directory = output / model
    if source:
        lock = (json.loads(prepare_query_encoder.LOCK_PATH.read_text()) if model == 'gemma'
                else prepare_embeddings.LOCK)
        for name in lock['files']:
            original = (source / name).resolve(strict=True)
            original.relative_to(source.resolve())
            destination = directory / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, destination)
            destination.chmod(0o644)
    if model == 'gemma':
        prepare_query_encoder.prepare(directory, verify_only=verify_only or bool(source), mirror=mirror)
    else:
        prepare_embeddings.prepare(output=directory, verify_only=verify_only or bool(source), mirror=mirror)
    if not verify_only:
        output.mkdir(parents=True, exist_ok=True)
        marker.write_text(json.dumps({'model': model}) + '\n')
        marker.chmod(0o644)
        (output / 'model').write_text(model + '\n')
        (output / 'model').chmod(0o644)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--model', choices=['gemma', 'e5'], required=True)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--mirror')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    try:
        prepare(args.output, args.model, args.source, args.mirror, args.verify_only)
    except Exception:
        print('Cache preparation failed: inspect the source snapshot or mirror privately', file=sys.stderr)
        return 1
    print('Pinned model cache verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
