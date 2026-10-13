# EmbeddingGemma 2 CPU passage sample

Date: 2026-10-13
Status: observed

This bounded local sample informs the single-machine evaluation guide. It is not
a CI performance threshold or a claim about complete ingestion throughput.

| Setting | Observed value |
| --- | --- |
| Model | google/embeddinggemma-2 |
| Source revision | 914f7f89142e33e77833254d9c9b90c3cef7303b |
| Dimensions | 768, normalized float32 vectors |
| CPU | Intel Xeon at 2.90 GHz; VM exposes 8 vCPUs |
| Service allocation | Affinity restricted to 4 cores, 4 PyTorch threads |
| Runtime | Python 3.12.13, torch 2.8.0+cpu, sentence-transformers 6.1.0, transformers 5.19.0 |
| Input | Synthetic title/body; 6,634 UTF-8 bytes, 1,533 model tokens |
| Batch/concurrency | One passage/request, one request at a time |
| Warmup | Model loader warmup, then one measured-shape request (2.131 s) |
| Timed sample | 8 requests in 14.648020 s |
| Throughput | 0.546149 passages/s |

Model assets passed the existing SHA-256 lock. The same CPU loader and authenticated
HTTP adapter used by the deployment served these requests natively because the VM
cannot enter the container runtime's cgroup. The endpoint reported its full model
revision, dimensions and runtime versions before timing began. No GPU or network
model access was used during serving. The measurement's `--tokens 512` builds a
synthetic repeat-count assumption; offline tokenization of the exact input found
1,533 actual model tokens. It does not represent a 512-token passage measurement.

Method: prepare the locked snapshot, start `deploy.cpu.embedding_server` with four
threads and four-core affinity, then run `scripts/measure_cpu_embeddings.py` with
eight requests, one warmup and a 40-second maximum timed window. Count the exact
input with the snapshot's tokenizer; exclude model download/load from throughput.
The sample completed in under a minute and all requests fit the provider's
ten-second request limit. Detailed JSON is retained as ticket evidence.

This long repeated input is useful for bounding individual CPU requests, but it
does not characterize multilingual content, mixed lengths, concurrent queries,
packing, a complete import, or memory/disk use. Size those independently. At three
passages/document, `documents × 3 / passages_per_second` estimates encoding time
only when the measured passage shape matches the actual workload. Do not apply
the measured rate as a guaranteed CPU scaling coefficient.
