package postgres

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"strings"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/history"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

// HistoryStore compacts detail without removing replay or monitoring identities.
type HistoryStore struct{ Pool *pgxpool.Pool }

var _ history.Store = HistoryStore{}

// PruneHistory gives every table a turn even when a protected row or a busy
// Organization blocks another table. Each transaction processes one Organization
// and at most batch candidates; checkpoints advance over retained rows too.
func (s HistoryStore) PruneHistory(ctx context.Context, p history.Policy, batch int) (int, error) {
	if p.Disabled {
		return 0, nil
	}
	if batch < 1 || batch > 1000 || p.ImportDetail <= 0 || p.AlertDetail <= 0 {
		return 0, errors.New("invalid history retention policy")
	}
	total := 0
	var failure error
	for _, stage := range historyStages {
		if ctx.Err() != nil {
			return total, errors.Join(failure, ctx.Err())
		}
		n, err := s.historyBatch(ctx, p, stage, batch)
		total += n
		if err != nil {
			failure = errors.Join(failure, fmt.Errorf("history %s: %w", stage.kind, err))
		}
	}
	return total, failure
}

type historyStage struct {
	kind, table, keys, guard, mutation string
	imports, clock                     bool
}

// Scalar point probes intentionally exclude whole-table hash alternatives.
const historyWatermark = `COALESCE((SELECT p.pruned_through FROM change_journal_prunes p WHERE p.organization=c.organization),0)`
const historyPendingEvaluation = `COALESCE((SELECT true FROM evaluation_intents i WHERE i.organization=c.organization AND i.record_version_id=c.record_version_id AND i.state='pending' LIMIT 1),false)`

// The earliest decided evaluation per pair is a permanent deduplication fact.
// Keeping it also protects events still undispatched and later Version reverts.
var historyStages = []historyStage{
	{kind: "receipts", table: "ingestion_receipts", keys: "organization,id", imports: true,
		guard: `c.state='resolved' AND c.accepted_at<now()-make_interval(secs=>$4::double precision)
 AND (octet_length(c.canonical_request)>0 OR c.command<>'{}'::jsonb)
 AND (octet_length(c.request_digest)=32 OR (c.request_digest IS NULL AND octet_length(c.canonical_request)>0))
 AND NOT COALESCE((SELECT NOT o.dispatched FROM ingestion_outbox o WHERE (o.organization,o.receipt_id)=(c.organization,c.id)),false)
 AND NOT COALESCE((SELECT NOT o.dispatched FROM bulk_ingestion_outbox o WHERE (o.organization,o.receipt_id)=(c.organization,c.id)),false)`,
		mutation: `UPDATE ingestion_receipts h SET request_digest=COALESCE(h.request_digest,sha256(h.canonical_request)),canonical_request=''::bytea,command='{}'::jsonb`},
	{kind: "revisions", table: "accepted_revisions", keys: "organization,record_id,slot", imports: true,
		guard: `c.command<>'{}'::jsonb AND c.accepted_at<now()-make_interval(secs=>$4::double precision)
 AND COALESCE((SELECT (` + deadVersionSQL + `) AND NOT v.quarantined AND v.processing='idle'
 FROM record_versions v JOIN LATERAL (SELECT * FROM records r WHERE (r.organization,r.id)=(v.organization,v.record_id) LIMIT 1) r ON true
 WHERE (v.organization,v.id)=(c.organization,c.version_id) LIMIT 1),false)
 AND NOT COALESCE((SELECT true FROM ingestion_receipts rc WHERE rc.organization=c.organization AND rc.record_id=c.record_id AND rc.slot=c.slot AND rc.state='pending' LIMIT 1),false)`,
		mutation: `UPDATE accepted_revisions h SET command='{}'::jsonb`},
	{kind: "evaluations", table: "evaluation_intents", keys: "organization,subscription_version_id,sequence", clock: true,
		guard: `c.state='done' AND c.retention_started_at<now()-make_interval(secs=>$4::double precision)
 AND c.sequence<=COALESCE((SELECT p.position FROM monitoring_checkpoints p WHERE p.organization=c.organization),0)
 AND (c.kind<>'evaluation' OR c.outcome NOT IN ` + decidedOutcomes + ` OR COALESCE((
  SELECT true FROM evaluation_intents d WHERE d.organization=c.organization
   AND d.subscription_version_id=c.subscription_version_id AND d.record_version_id=c.record_version_id
   AND d.sequence<c.sequence AND d.kind='evaluation' AND d.state='done' AND d.outcome IN ` + decidedOutcomes + ` LIMIT 1),false))
 AND NOT ` + historyPendingEvaluation + `
 AND COALESCE((SELECT ` + deadVersionSQL + ` FROM record_versions v
 JOIN LATERAL (SELECT * FROM records r WHERE (r.organization,r.id)=(v.organization,v.record_id) LIMIT 1) r ON true
 WHERE (v.organization,v.id)=(c.organization,c.record_version_id) AND NOT v.quarantined LIMIT 1),false)`,
		mutation: `DELETE FROM evaluation_intents h`},
	{kind: "notices", table: "monitoring_notices", keys: "organization,event_id", clock: true,
		guard:    `octet_length(c.body)>0 AND c.delivery_id IS NULL AND c.retention_started_at<now()-make_interval(secs=>$4::double precision) AND c.position<=` + historyWatermark,
		mutation: `UPDATE monitoring_notices h SET body=''::bytea`},
	{kind: "matches", table: "matches", keys: "organization,id", clock: true,
		guard: `c.evidence<>'null'::jsonb AND c.retention_started_at<now()-make_interval(secs=>$4::double precision) AND c.position<=` + historyWatermark + `
 AND NOT COALESCE((SELECT true FROM deliveries d WHERE d.organization=c.organization AND d.match_id=c.id AND d.state<>'delivered' LIMIT 1),false)
 AND NOT ` + historyPendingEvaluation,
		mutation: `UPDATE matches h SET evidence='null'::jsonb`},
}

func (s HistoryStore) historyBatch(parent context.Context, p history.Policy, stage historyStage, batch int) (int, error) {
	ctx, cancel := context.WithTimeout(parent, 4*time.Second)
	defer cancel()
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return 0, err
	}
	defer func() {
		cleanup, cancel := context.WithTimeout(context.WithoutCancel(ctx), 500*time.Millisecond)
		defer cancel()
		_ = tx.Rollback(cleanup)
	}()
	if _, err = tx.Exec(ctx, `SET LOCAL lock_timeout='100ms'; SET LOCAL statement_timeout='3s'`); err != nil {
		return 0, err
	}
	// An ordinary application write initializes only this stage's checkpoint.
	// The transaction deadline also bounds conflicts with another worker.
	if _, err = tx.Exec(ctx, `INSERT INTO history_retention_progress(kind) VALUES($1) ON CONFLICT DO NOTHING`, stage.kind); err != nil {
		return 0, err
	}
	var cursor json.RawMessage
	err = tx.QueryRow(ctx, `SELECT cursor FROM history_retention_progress WHERE kind=$1 FOR UPDATE SKIP LOCKED`, stage.kind).Scan(&cursor)
	if errors.Is(err, pgx.ErrNoRows) {
		return 0, nil
	}
	if err != nil {
		return 0, err
	}
	keys := strings.Split(stage.keys, ",")
	parts := make([]string, len(keys))
	for i, key := range keys {
		parts[i] = fmt.Sprintf("COALESCE($1::jsonb->>%d,'')", i)
		if key == "sequence" {
			parts[i] = fmt.Sprintf("COALESCE(($1::jsonb->>%d)::bigint,0)", i)
		}
	}
	keyCursor := strings.Join(parts, ",")
	var org string
	err = tx.QueryRow(ctx, `SELECT organization FROM `+stage.table+` WHERE (`+stage.keys+`)>(`+keyCursor+`) ORDER BY `+stage.keys+` LIMIT 1`, cursor).Scan(&org)
	if errors.Is(err, pgx.ErrNoRows) {
		_, err = tx.Exec(ctx, `UPDATE history_retention_progress SET cursor='[]' WHERE kind=$1`, stage.kind)
		if err == nil {
			err = tx.Commit(ctx)
		}
		return 0, err
	}
	if err != nil {
		return 0, err
	}
	// Writers changing eligibility always take the journal before row locks.
	if err = lockJournal(ctx, tx, org); err != nil {
		return 0, err
	}
	age := p.AlertDetail
	if stage.imports {
		age = p.ImportDetail
	}
	candidate := `WITH candidates AS MATERIALIZED (SELECT * FROM ` + stage.table + ` WHERE organization=$2 AND (` + stage.keys + `)>(` + keyCursor + `) ORDER BY ` + stage.keys + ` LIMIT $3 FOR UPDATE), `
	pairsH, pairsC := []string{}, []string{}
	desc := []string{}
	for _, key := range keys {
		pairsH = append(pairsH, "h."+key)
		pairsC = append(pairsC, "c."+key)
		desc = append(desc, key+" DESC")
	}
	join := `(` + strings.Join(pairsH, ",") + `)=(` + strings.Join(pairsC, ",") + `)`
	if stage.clock {
		// First observation starts a full window, conservatively for old and
		// previous-binary rows too. Clock initialization and reclamation target
		// disjoint rows of this bounded, locked candidate page.
		candidate += `clocked AS (UPDATE ` + stage.table + ` h SET retention_started_at=now()
 FROM candidates c WHERE ` + join + ` AND c.retention_started_at IS NULL RETURNING 1), `
	}
	mutation := stage.mutation + ` FROM candidates c WHERE ` + join + ` AND ` + stage.guard + ` RETURNING 1`
	if strings.HasPrefix(stage.mutation, "DELETE") {
		mutation = stage.mutation + ` USING candidates c WHERE ` + join + ` AND ` + stage.guard + ` RETURNING 1`
	}
	query := candidate + `mutated AS (` + mutation + `) SELECT
 COALESCE((SELECT jsonb_build_array(` + stage.keys + `) FROM candidates ORDER BY ` + strings.Join(desc, ",") + ` LIMIT 1),'[]'::jsonb),(SELECT count(*) FROM mutated)`
	var removed int
	err = tx.QueryRow(ctx, query, cursor, org, batch, age.Seconds()).Scan(&cursor, &removed)
	if err != nil {
		return 0, err
	}
	if _, err = tx.Exec(ctx, `UPDATE history_retention_progress SET cursor=$2 WHERE kind=$1`, stage.kind, cursor); err != nil {
		return 0, err
	}
	return removed, tx.Commit(ctx)
}
