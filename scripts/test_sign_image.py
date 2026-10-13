"""The shell signing boundary must stop on every signing/verification failure."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ImageSigning(unittest.TestCase):
    def test_every_operation_is_required_and_errors_propagate(self):
        operations = ['sign', 'verify', 'attest', 'verify-attestation']
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            executable = root / 'cosign'
            executable.write_text('''#!/usr/bin/env python3
import json, os, sys
with open(os.environ['CALLS'], 'a') as log:
    log.write(json.dumps(sys.argv[1:]) + '\\n')
print('{}')
if sys.argv[1] == os.environ.get('FAIL_OPERATION'):
    sys.exit(int(os.environ['FAIL_STATUS']))
''')
            executable.chmod(0o755)
            calls = root / 'calls'
            image = 'registry.example.invalid/image@sha256:' + 'a' * 64
            identity = 'https://github.com/example/repository/.github/workflows/release.yml@refs/tags/v1'
            cases = [(None, 0, False), (None, 0, True)]
            cases += [(operation, status, True) for operation in operations for status in [1, 124, 137]]
            for operation, status, key_mode in cases:
                with self.subTest(operation=operation, status=status, key_mode=key_mode):
                    calls.write_text('')
                    args = ['bash', str(ROOT / 'scripts/sign_image.sh'), image, 'sbom.json']
                    if key_mode:
                        args += ['private.key', 'public.key']
                    result = subprocess.run(args, capture_output=True, text=True, timeout=5,
                                            env={**os.environ, 'PATH': folder + os.pathsep + os.environ['PATH'],
                                                 'CALLS': str(calls), 'FAIL_OPERATION': operation or '',
                                                 'FAIL_STATUS': str(status), 'COSIGN_CERTIFICATE_IDENTITY': identity})
                    self.assertEqual(result.returncode, status, result.stderr)
                    emitted = [json.loads(line) for line in calls.read_text().splitlines()]
                    expected = operations if operation is None else operations[:operations.index(operation) + 1]
                    self.assertEqual([args[0] for args in emitted], expected)
                    for args in emitted:
                        self.assertIn(image, args)
                        self.assertEqual(args[-2:], ['--timeout', '60s'])
                        self.assertFalse(any(arg.startswith(('--insecure', '--tlog-upload=false')) for arg in args))
                        if args[0].startswith('verify'):
                            if key_mode:
                                self.assertEqual(args[args.index('--key') + 1], 'public.key')
                            else:
                                self.assertEqual(args[args.index('--certificate-identity') + 1], identity)
                                self.assertEqual(args[args.index('--certificate-oidc-issuer') + 1],
                                                 'https://token.actions.githubusercontent.com')


if __name__ == '__main__':
    unittest.main()
