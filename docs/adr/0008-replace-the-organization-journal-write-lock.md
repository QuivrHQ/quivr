# Replace the organization journal write lock

Date: 2026-10-13

Status: accepted

## Decision

Redesign ingestion so independent writers append unnumbered event intents with their canonical changes, and one sequencer publishes the committed events. Preserve commit order, replay, idempotency and the supported application rollback window. Do not add another producer batching layer before proving the replacement.

Prefer plain SQL when it can satisfy those guarantees. The transaction-ID/snapshot-horizon design evaluated below provides a complete prefix in transaction-ID order, but cannot reconstruct commit order. Choose PostgreSQL logical decoding as the candidate source of commit order, subject to correctness and deployment proofs. This record authorizes the direction and proposes implementation slices; it does not enable a new writer mode or claim a throughput improvement.

Logical decoding is a substantial operational dependency. Keep the existing synchronous journal usable on ordinary PostgreSQL and leave the new mode disabled by default until an operator explicitly enables it on a proven stack. Hosts without decoding support remain usable with the current mechanism; they do not inherit the future throughput target. If decoding cannot be made portable and reproducible within that opt-in deployment contract, revisit the architecture rather than silently weaken ordering or require unsupported host privileges.

## Why replace it

The current [journal implementation](../../internal/adapters/postgres/content.go) holds one organization row through the writer's commit, including its WAL flush. Independent records in that organization therefore queue behind each other. Moving preparation before the lock and grouping some writes shortened or amortized that critical section without removing it. Fresh measurements after the hot-table maintenance fix still identified this lock as the ingestion ceiling; deployment-specific evidence remains in the issue tracker.

The row also fences domain decisions: request replay, revision reservation, acceptance order, current-version selection, withdrawal, monitoring boundaries and administrative cutover. Removing event numbering alone would leave those decisions unprotected. This record supersedes the organization-wide lock mechanism described in [ADR 0003](0003-revert-to-earlier-content-mints-a-new-record-version.md), while preserving its A/B/A′ correction, immutable lineage and event-identity decisions and [ADR 0002](0002-record-version-identity-from-submitted-input.md).

The [change-feed contract](../../contracts/http/v0/openapi.yaml) requires commit order, resumable cursors and an exact start-now position. A published journal head must cover a complete committed prefix: readers and evaluation checkpoints cannot skip an event that appears later below a cursor already returned. Publication order must follow canonical transaction commits, not merely the order the sequencer discovers rows.

## Alternatives

### Plain-SQL transaction horizon

Each writer inserts logged intents in the canonical transaction with its top-level `pg_current_xact_id()` (`xid8`), stable mutation identity and intra-transaction ordinal. The single sequencer takes a fresh primary snapshot and captures `pg_snapshot_xmin(pg_current_snapshot())`. It selects MVCC-visible intents strictly below that horizon and publishes complete transactions in increasing transaction-ID order, then ordinal order. Publication, assigned positions and the durable processed watermark commit together. Bounded pages cannot advance the watermark beyond unprocessed intents or split a source transaction's publication.

This has real advantages. Ordinary application SQL and function access suffice; it needs no logical WAL setting, publication, replication connection, slot, replication role or commit-timestamp setting. Transaction rollback removes intents along with canonical changes. Savepoint rollback removes the corresponding intents; the surviving ones retain their top-level transaction identity. A stopped sequencer accumulates ordinary table rows, and recovery reads them without preserving a separate WAL stream. It fits additive tables and application backfill, and has less operational work on managed hosts.

The horizon provides completeness, not commit order. PostgreSQL assigns [transaction IDs at first write](https://www.postgresql.org/docs/17/transaction-id.html). The [snapshot minimum](https://www.postgresql.org/docs/17/functions-info.html#FUNCTIONS-PG-SNAPSHOT) bounds transactions already completed, including aborted transactions; visible rows distinguish committed intents from dead ones. Neither records the relative order of the completed commits.

Consider this valid execution, with one intent per transaction:

| Step | Transaction A | Transaction B | Sequencer |
| --- | --- | --- | --- |
| 1 | Allocate ID 100; append intent; stay open | | |
| 2 | | Allocate ID 101; append intent; commit | |
| 3 | Still open | Committed | Horizon is 100: neither intent qualifies |
| 4 | Commit | | |
| 5 | Committed | Committed | Horizon is 102: both qualify; ID order is A, B |

Actual commit order is B, A. A safe watermark removes the missing-row race but does not repair this inversion. If A instead commits before B and both finish before the next poll, the intent rows and final snapshot are the same. The sequencer cannot distinguish these histories using transaction IDs and visibility alone. Ordering by the polling round also loses order within a round. This is a correctness counterexample derived from documented semantics, not a local performance result.

Latency is at least the polling delay plus the lifetime of any older transaction holding the horizon. A long-running writer or prepared transaction can delay otherwise committed work, including unrelated organizations; XIDs are cluster-wide. Fresh short sequencer transactions avoid pinning their own old horizon, but cannot force other transactions to finish. Transaction timeouts can bound cooperative writers, at the cost of aborting them; they supply no missing commit-order information.

Rollback is simpler operationally than decoding: pending rows, watermark and published positions live in the database and need no slot recovery. Both binaries must still understand the mode, pending references and watermark, and use the same cutover fence. Stored XIDs are local transaction identities, so logical dump/restore into another cluster needs an explicit pending-intent recovery boundary; they cannot become public cursors or be compared blindly with the new cluster's horizon. Simpler recovery does not overcome the ordering failure.

Commit timestamps are not a portable repair: [their tracking requires configuration and their history is pruned](https://www.postgresql.org/docs/17/functions-info.html#FUNCTIONS-COMMITTED-TXID), and a wall-clock timestamp with an XID tie-breaker does not establish exact commit-log order. Reading a WAL position before commit or writing an ordering marker after commit also leaves a race. Serializing writers through commit restores order but restores the bottleneck. Reframing the contract as transaction-ID or observation order would be a separate public-contract decision, outside this work.

### Logical decoding

Writers insert the same transactional intents without assigning public positions. One decoder reads their committed transactions using PostgreSQL's built-in `pgoutput`, initially with in-progress streaming and two-phase decoding disabled. PostgreSQL [decodes concurrent transactions in commit order](https://www.postgresql.org/docs/17/logicaldecoding-output-plugin.html); rolled-back transactions are excluded. The publisher follows source commit order and explicit intent ordinals within each transaction, assigning the existing organization-scoped positions.

An open writer does not force already committed unrelated writers to wait for its XID to leave a snapshot horizon. Publication still costs decoding/dispatch delay and a durable publisher commit; long transactions can increase decoder storage and retained WAL. This is a latency advantage over the horizon scheme, not a measured guarantee of the ingestion target.

The deployment cost is higher: [logical WAL settings and slot/sender capacity](https://www.postgresql.org/docs/17/logical-replication-config.html), publication ownership/setup, [a replication-capable role and connection authorization](https://www.postgresql.org/docs/17/logical-replication-security.html), a direct replication connection, and lifecycle management for the slot. Ordinary application credentials or a transaction-pooling endpoint do not imply this access. Managed-host support must be checked explicitly; the first slice must produce a reproducible local setup and establish which supported hosts permit it.

[Slots survive crashes, can replay changes and retain WAL/catalog resources](https://www.postgresql.org/docs/17/logicaldecoding-explanation.html). Monitor publication lag, retained WAL and disk capacity, and set an operator-chosen retention bound with an explicit response to slot invalidation. Never acknowledge source progress before durable publication. Slot loss, failover without the required source history, or a missing prefix must stop publication and surface recovery work; recreating a slot and sorting leftover SQL intents cannot recover the lost commit order. Pending intents alone are insufficient. Checkpoints, slot state and database recovery must stay consistent across backup, restore and failover. The deployment proof must cover slot bootstrap/drain, interruption and recovery, and retire an unused slot only after its source responsibility is safely discharged.

Both alternatives need a bridge release before activation to preserve mixed-version safety. Decoding additionally requires that bridge binary to understand the decoder, pending references and slot recovery so application rollback does not abandon accepted events or leave an unowned retaining slot.

### Comparison and selection

| Concern | Plain SQL with XID horizon | Logical decoding |
| --- | --- | --- |
| Complete published prefix | Yes, with visibility, strict horizon and atomic watermark | Yes, with complete source commits and atomic publication/checkpoint |
| Canonical commit order | No: XID allocation and commit can invert | Yes: consume committed transactions in decoder order |
| Aborted transactions | No visible intents; gaps require no invented events | Excluded from committed decoding |
| Long-running transactions | Can stall the common horizon and later work | Can retain source WAL; committed later writers can publish |
| Normal latency | Polling plus horizon wait plus publisher commit | Decode/dispatch plus publisher commit |
| Deployment | Application SQL; table growth and pending-row recovery | Logical WAL, replication access, publication, slot retention/recovery |
| Application rollback | Bridge must honor mode and pending references | Same, plus decoder and source-slot responsibility |

Plain SQL wins operationally but fails a required invariant. Logical decoding is therefore the eligible replacement candidate of these two, while the existing journal remains the portable default. A broker or a single command executor would add infrastructure or move the serialized commit bottleneck; neither is justified without another measured, approved design. Correctness and deployment gates precede enablement, and failure of either gate reopens this decision.

## Publication and domain safety

“Lock-free append” means independent writers no longer share the organization journal row. Record/request uniqueness and scoped entity locks remain necessary; document their acquisition order. Retain routing and corpus lifecycle fences where required. Persist canonical changes, full immutable event payload/references, ingestion dispatch responsibility and queue observations atomically. Preserve request canonicalization and same-key replay/conflict behavior, receipt resolution, Source Position handling and correction-versus-withdrawal arbitration.

Only one active publisher may assign positions. Fence ownership durably, publish complete source transactions in order, resolve their position-dependent references, and commit events, head and source checkpoint atomically. Exclude publisher output from the decoded input. It may amortize its own flush over a bounded committed prefix without adding a producer batching layer. A crash before publication leaves the source retryable; after publication, source replay recognizes the durable checkpoint/mutation identity and reuses existing positions. Retain deduplication/checkpoint evidence beyond event pruning so replay cannot resurrect expired events.

New transitions need immutable mutation identities independent of assigned positions. Existing monitoring toggles derive identity from the previous opposite transition's position; repeated pending toggles cannot safely use that rule. Assign a durable identity to each new logical mutation before append, reuse it on request replay, and preserve all existing historical event IDs.

Canonical state can include newer changes whose journal boundaries remain pending. Keep a durable pending-publication reference per affected resource, or equivalent published state. Position-sensitive fan-out, match decisions, delivery admission, listing and pruning defer affected work rather than interpret a NULL or old position as current. Resolve current references only when the immutable mutation identity still matches: publishing an earlier transition preserves its history without overwriting or clearing a newer pending transition. Subscription activation, enable/edit boundaries, match ordering and monitoring checkpoints must all use the published prefix. Never backfill the paused interval after re-enable.

Start-now uses an ordered committed barrier and waits for its publication before returning the organization prefix position. Polling/SSE exposes only complete published prefixes. Commands whose success currently depends on journal publication wait for their own publication after releasing their canonical transaction; never hold entity locks while awaiting the sequencer. A timeout after canonical commit has an ambiguous committed outcome recoverable by the original request key. Do not duplicate canonical work because the publisher is behind.

## Rollout and rollback

Follow [the migration policy](../agents/migrations.md): additive tables/compatible optional columns, no procedural SQL or triggers, resumable application backfill, and no down migration or edit to released SQL. Concrete database object names and migration timestamps are reserved on the implementation tickets.

Release N is the compatibility bridge. It understands both writer modes, barriers, pending references, publication and recovery, but keeps the existing journal mode enabled while pre-bridge binaries remain possible. Mixed pre-bridge/N writers use that existing mechanism. Pre-bridge writers produce no intents; complete shadow comparison starts only after those processes and transactions drain, at a recorded source/journal boundary. Expanded-schema and previous-binary write/restart proofs remain required.

Release N+1 may explicitly enable sequencing after the bridge has shipped, capabilities/proofs pass and all pre-bridge processes and transactions drain. Both N and N+1 must honor durable mode through a shared/exclusive application cutover fence acquired before domain locks. Switching modes drains admitted writers; direct-journal and sequenced writers cannot coexist within an organization mode. Record the source boundary and old committed head, then continue above that head without renumbering history or changing existing cursors. Keep global source checkpointing consistent even if organizations activate separately.

Rollback from N+1 to N must keep new-mode reads, writes and recovery working. Turning the mode back to the existing journal is a separate fenced drain operation that publishes all pending source transactions before handing head ownership back; it must not happen automatically on decoder error. Rollback to pre-bridge software after activation is outside that window and requires explicit operator guidance. Remove obsolete schema only in a later, opt-in contract after older binaries retire. If these transitions cannot be proven, leave sequencing disabled.

## Proposed implementation slices

Implementation follows coordinator approval of separate tickets, linked by native blocking relations. This ADR adds no batching layer, migration, runtime setting, test or API change.

1. **Prove ordering and deployment support.** On the pinned PostgreSQL version, reproduce the inverted-commit XID counterexample and horizon stall; prove decoder ordering with delayed commits, abort/savepoint rollback, multiple ordinals and source/publisher reconnects. Produce a local setup anyone can reproduce without private resources, inventory hosting permissions/settings, and measure baseline versus sequencing capacity. Proceed only if exact order and practical host support hold; otherwise propose another design.
2. **Ship the bridge and shadow journal.** Add compatible durable intents, mode/ownership and checkpoint state, decoder setup/runtime and shadow comparison. Inventory every event producer and stored-position consumer, including batch and audit paths. Prove expanded-schema previous-binary writes, mixed binaries in existing mode, previous-binary restart, source bootstrap boundary and fail-closed recovery. Depends on slice 1; sequencing stays disabled.
3. **Allow independent records to commit concurrently.** Replace domain reliance on the organization fence with scoped locks and unique claims across acceptance, publication, availability and withdrawal. Migrate subscription boundaries, matches/notices, pruning, retention and routing/corpus cutover together, including immutable toggle identities and pending-state gating. Prove same-key convergence/conflict, A/B/A′, correction versus withdrawal, and independent progress. Stall sequencing through disable/enable/disable/enable while dispatch/admission run: no backfill, collision or earlier publication clearing newer pending state. Depends on slice 2; new mode remains disabled.
4. **Activate and roll back safely.** In N+1, implement fenced cutover above the existing head, complete-transaction publication, command/start-now barriers, publisher failover, deduplication and retention. Prove N/N+1 mixed operation and rollback to N, mode reversal after drain, crashes before/after publication and acknowledgement, and filtered-cursor/pruning safety. Depends on slice 3 and a previously shipped bridge release.
5. **Measure and retire replaced paths.** Compare the same neutral reference workload/hardware with durable commits (`synchronous_commit=on`) and acceptance concurrency 1/8/32. Target about 200 accepted items/s per organization locally with no growing publication backlog or correctness loss; distinguish acceptance, materialization and search availability. Record sustained rates, publication lag, latency percentiles, errors, WAL/lock waits, CPU/I/O and search under import. Preserve the separate burst and search-under-import contracts. If the target is missed, identify the measured bottleneck before adding mechanisms. Remove obsolete writer batching/retry/fallback paths only after replacement proofs; destructive SQL needs a later contract. Depends on slice 4.

The throughput target and decoder deployment support remain unproven. The new journal must earn enablement with those measurements and correctness/rollback evidence; this decision alone changes no installation.
