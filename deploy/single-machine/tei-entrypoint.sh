#!/bin/sh
set -eu
if [ "$(cat /models/model)" != e5 ]; then
  echo 'E5 cache identity mismatch; use a fresh installation' >&2
  exit 1
fi
sha256sum --check --status /app/e5.sha256 || { echo 'E5 cache verification failed' >&2; exit 1; }
export HF_HUB_OFFLINE=1
exec text-embeddings-router --model-id /models/e5 --dtype float32 --pooling mean \
  --max-client-batch-size 32 --max-batch-tokens 8192 --auto-truncate false --tokenization-workers 2
