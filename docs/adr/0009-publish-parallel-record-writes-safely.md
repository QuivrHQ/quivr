# Publish parallel Record writes safely

Date: 2026-10-13

Status: accepted

## Decision

Supersede [ADR 0008](0008-replace-the-organization-journal-write-lock.md) with a portable SQL journal. Independent Records may commit concurrently in an Organization. Events retain unique durable identities and stable traversal order; events for one Record keep their order. Concurrent writes to different Records have no strict commit-order guarantee. This deliberate contract change removes the need for logical decoding, replication access, slots, triggers or procedural SQL. The correction identities and A/B/A′ lineage in [ADR 0003](0003-revert-to-earlier-content-mints-a-new-record-version.md) remain unchanged.

The bridge defaults to the legacy journal. Parallel mode is an explicit deployment-wide cutover after retiring pre-bridge binaries. Those binaries assume the organization head is synchronous, so they cannot coexist with activated parallel writers. Both supported binaries at activation must understand the durable mode. Rollback to the bridge honors it.

## Numbering and publication

A `CACHE 1` bigint sequence assigns positions in each canonical transaction. Every writer assigns its top-level XID before taking a number. Aborts and publisher barriers leave gaps; callers persist actual assigned positions rather than infer a contiguous range. Writers retain routing and corpus fences, request claims, sorted Record arbitration and scoped Subscription/Operation/delivery locks. They never update an organization journal head in parallel mode.

A publisher samples a sequence barrier B in a completed short transaction. In a separate new top-level transaction, it first assigns XID X, then saves B/X with a mode-epoch CAS. Every writer capable of owning a position below B therefore obtained its XID before X. A later primary snapshot with xmin greater than X proves all those writers have finished. Only then may the durable safe head advance through B. The barrier itself is a gap.

This proof depends on [sequence cache semantics](https://www.postgresql.org/docs/17/functions-sequence.html), [top-level XID allocation](https://www.postgresql.org/docs/17/transaction-id.html) and [snapshot visibility](https://www.postgresql.org/docs/17/functions-info.html#FUNCTIONS-PG-SNAPSHOT). It is an inference from those semantics, exercised by real PostgreSQL owner tests. A visible event maximum, or a filter on event XIDs alone, is insufficient: an older XID can receive a higher sequence while an invisible lower number remains open. Recovery keeps the oldest pending valid observation; it never replaces it on every poll or reconstructs progress from visible maxima.

Feed polling/SSE, evaluation checkpoints, Match listing, delivery admission, retirement and retention/pruning use the safe prefix. Canonical Subscription edits ahead of it defer dispatch and decisions instead of being filtered away. Re-enabling still evaluates future triggers only, without backfilling the pause. Writers record queue changes in a Record-scoped dirty ledger; independent bounded reconciliation locks aggregate stripes before observations and atomically acknowledges the applied revision. Snapshot publication does not stamp incomplete counts as fresh.

## Starts, latency and recovery

An exact start captures the primary snapshot and safe head, then a sequence ceiling. Its signed cursor carries a short-lived scope-bound reference. Reads exclude events already visible in that snapshot and retain then-in-flight writers, including lower numbers that commit later. Start references pin pruning until the safe prefix passes the ceiling or their retention expires. Old numeric cursors remain valid. Missing or expired references require explicit resynchronization.

API and worker processes poll publication every 100 ms. PostgreSQL 17 transaction timeouts bound engine transactions from BEGIN, default 30 seconds. On a healthy database with no outside transaction pinning xmin, publication waits at most the longest configured engine transaction lifetime plus two poll intervals. Other clients, prepared transactions or database unavailability can break that latency bound; publication fails closed and reports allocation backlog and pending-observation age through `quivr journal status`. Ambiguous commits retain request-key recovery.

Activation holds queue maintenance then the exclusive writer-mode fence, drains contributions and initializes the sequence above every historical organization head. Reversal drains the same writers/contributions, publishes the completed allocation boundary and raises legacy heads before returning numbering to them. Sequence changes never overlap a bridge writer or sampler. Failed initialization can leave harmless unused sequence numbers, without renumbering history.

Logical backup/restore into another cluster invalidates stored XID snapshots. With every service stopped, `quivr journal restored --writers-drained` expires exact-start references, discards pending observations and establishes a drained prefix before restart. Numeric cursors and durable event IDs survive; clients holding invalidated snapshot cursors resynchronize. Ordinary runtime recovery never uses this offline maximum-based procedure.

Exactly-once means each journal fact has one durable identity and appears once in a forward cursor traversal. Reconnecting with an older cursor can repeat delivery; webhook transport and external side effects still require idempotency.
