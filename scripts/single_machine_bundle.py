"""Assemble the operator bundle from image digests that passed release checks."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import tarfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'deploy/single-machine'
spec = importlib.util.spec_from_file_location('single_machine_setup', SOURCE / 'setup.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


def assemble(images_directory, output, version, revision):
    output.mkdir(parents=True, exist_ok=True)
    gemma = json.loads((ROOT / 'third_party/query-encoder/model-lock.json').read_text())
    e5 = json.loads((ROOT / 'third_party/e5/model-lock.json').read_text())
    manifest = {'version': version, 'revision': revision, 'images': {},
                'models': {'gemma': gemma['source_revision'], 'e5': e5['model_revision']}}
    for component in setup.COMPONENTS:
        reference = (images_directory / ('quivr-' + component + '.txt')).read_text().strip()
        manifest['images'][component] = {'reference': reference, 'version': version, 'revision': revision}
    release = output / 'release.json'
    release.write_text(json.dumps(manifest, indent=2) + '\n')
    _, images = setup.release_images(release)
    for path in (SOURCE / 'setup.py', SOURCE / '.env.example', ROOT / 'deploy/infrastructure.py', ROOT / 'deploy/infrastructure.json'):
        shutil.copyfile(path, output / path.name)
    model = setup.stack(images, setup.infrastructure('small'), {
        'QUIVR_EMBEDDING': 'gemma', 'COMPOSE_PROJECT_NAME': 'quivr'})
    (output / 'compose.yaml').write_text(json.dumps(model, indent=2) + '\n')
    archive = output.parent / ('quivr-compose-' + version + '.tar.gz')
    with tarfile.open(archive, 'w:gz') as bundle:
        for path in sorted(output.iterdir()):
            if path.name in ('setup.py', '.env.example', 'infrastructure.py', 'infrastructure.json', 'release.json', 'compose.yaml'):
                bundle.add(path, arcname=path.name)
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--images', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--revision', required=True)
    args = parser.parse_args()
    print(assemble(args.images, args.output, args.version, args.revision))
