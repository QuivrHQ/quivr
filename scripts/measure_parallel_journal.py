#!/usr/bin/env python3
"""Bounded local relative acceptance evidence; no hosted providers or CI threshold.

Use an empty, task-owned loopback database named parallel_measure_<suffix>.
The JSON config stays private; neither connection strings nor errors containing
credentials are printed. The caller owns database creation and removal.
"""
import argparse
import json
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=pathlib.Path, required=True)
    parser.add_argument('--items', type=int, default=512)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.items <= 10000:
        parser.error('--items must be in 1..10000')
    scratch = ROOT / '.scratch'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='parallel-acceptance-', dir=scratch) as directory:
        binary = pathlib.Path(directory) / 'measure'
        subprocess.run(['go', 'build', '-o', str(binary), './tests/load/parallel-journal-acceptance'], cwd=ROOT, check=True)
        result = subprocess.run([str(binary), '--config', str(args.config.resolve()), '--items', str(args.items)], cwd=ROOT,
                                check=True, capture_output=True, text=True, timeout=310)
        report = json.loads(result.stdout)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    for trial in report['trials']:
        print(f"{trial['mode']:8} concurrency={trial['concurrency']:2} accepted/s={trial['accepted_items_per_second']:.1f} "
              f"p95_ms={trial['latency_p95_ms']:.1f} errors={trial['errors']}")


if __name__ == '__main__':
    main()
