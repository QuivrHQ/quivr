package postgres

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/operations"
	"github.com/The-Vibe-Company/quivr/internal/retrieval"
	"github.com/jackc/pgx/v5"
)

// Bound input records before applying coverage predicates. LIMIT on the missing
// output alone can still walk every covered record in a large corpus.
const rebuildValidationBatch = 256

const markRebuildRecordsSQL = `INSERT INTO projection_rebuild_dirty_records(organization,operation_id,record_id,version_id)
 SELECT DISTINCT r.organization,s.operation_id,r.id,COALESCE(r.current_version_id,'')
 FROM unnest($1::text[],$2::text[]) k(organization,record_id)
 JOIN records r ON (r.organization,r.id)=(k.organization,k.record_id)
 JOIN projection_rebuild_validation s ON (s.organization,s.corpus_id)=(r.organization,r.corpus_id)
 JOIN operations o ON (o.organization,o.id)=(s.organization,s.operation_id) AND o.state='running'
 ORDER BY r.organization,s.operation_id,r.id
 ON CONFLICT(organization,operation_id,record_id) DO UPDATE SET
 version_id=EXCLUDED.version_id,revision=projection_rebuild_dirty_records.revision+1,checked=false`

const markRebuildVersionSQL = `INSERT INTO projection_rebuild_dirty_records(organization,operation_id,record_id,version_id)
 SELECT v.organization,s.operation_id,v.record_id,COALESCE(r.current_version_id,'')
 FROM record_versions v JOIN records r ON (r.organization,r.id)=(v.organization,v.record_id)
 JOIN projection_rebuild_validation s ON (s.organization,s.corpus_id)=(r.organization,r.corpus_id)
 JOIN operations o ON (o.organization,o.id)=(s.organization,s.operation_id) AND o.state='running'
 WHERE v.organization=$1 AND v.id=$2 ORDER BY s.operation_id
 ON CONFLICT(organization,operation_id,record_id) DO UPDATE SET version_id=EXCLUDED.version_id,revision=projection_rebuild_dirty_records.revision+1,checked=false`

// Both generation overlays and rollback fallback selection participate in the
// gap predicate. Immutable plan identities alone do not capture an epoch swap.
var rebuildFingerprintSQL = `SELECT jsonb_build_object('epoch',COALESCE((SELECT epoch FROM routing_switch_state WHERE singleton),''),
 'plan',COALESCE((SELECT plan_id FROM active_pipeline_plan),''),'routed',to_jsonb(rg),'target',to_jsonb(tg))
 FROM operations o JOIN ` + effectiveGenerationsSQL + ` tg ON tg.id=o.target_generation_id
 JOIN ` + effectiveGenerationsSQL + ` rg ON rg.id=` + routedGenerationSQL("o.organization", "o.corpus_id") + `
 WHERE o.organization=$1 AND o.id=$2`

func rebuildFingerprint(ctx context.Context, tx pgx.Tx, org, id string) ([]byte, error) {
	var raw []byte
	err := tx.QueryRow(ctx, rebuildFingerprintSQL, org, id).Scan(&raw)
	return raw, err
}

// Registration drains previously admitted coverage preparation before enabling
// observation. It does no corpus scan and never queues an exclusive request.
func (s RebuildStore) initializeRebuildValidation(ctx context.Context, org, id string) (bool, error) {
	var exists bool
	if err := s.Pool.QueryRow(ctx, `SELECT EXISTS(SELECT FROM projection_rebuild_validation WHERE organization=$1 AND operation_id=$2)`, org, id).Scan(&exists); err != nil || exists {
		return exists, err
	}
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return false, err
	}
	defer tx.Rollback(ctx)
	var acquired bool
	if err = tx.QueryRow(ctx, `SELECT pg_try_advisory_xact_lock($1)`, projectionRoutingLock).Scan(&acquired); err != nil || !acquired {
		return false, err
	}
	if err = lockJournal(ctx, tx, org); err != nil {
		return false, err
	}
	op, err := lockOperation(ctx, tx, org, id)
	if err != nil {
		return false, err
	}
	if op.State != operations.StateRunning {
		return false, operations.ErrNotRunning
	}
	fingerprint, err := rebuildFingerprint(ctx, tx, org, id)
	if err != nil {
		return false, err
	}
	_, err = tx.Exec(ctx, `INSERT INTO projection_rebuild_validation(organization,operation_id,corpus_id,fingerprint) VALUES($1,$2,$3,$4) ON CONFLICT DO NOTHING`, org, id, op.CorpusID, fingerprint)
	if err != nil {
		return false, err
	}
	return true, tx.Commit(ctx)
}

// Owner compatibility intentionally includes current ineligible versions too,
// preserving activation's original population independently of gap eligibility.
var rebuildOwnerGapSQL = `EXISTS(SELECT FROM ` + effectiveGenerationsSQL + ` tg
 JOIN projection_coverage pc ON (pc.organization,pc.version_id,pc.generation_id)=(v.organization,v.id,tg.id) AND ` + effectiveCoverageSQL("pc") + `
 JOIN accepted_revisions ar ON (ar.organization,ar.record_id,ar.slot)=(v.organization,v.record_id,v.slot)
 WHERE tg.id=$3 AND $4::jsonb->>'default'<>''
 AND pc.plugin_id<>COALESCE(tg.ingestion_routing->'routes'->>COALESCE(NULLIF(ar.source_media_type,''),'text/plain'),tg.ingestion_routing->>'default',''))`

type rebuildValidationRecord struct {
	record, version string
	gap, ownerGap   bool
}

func (s RebuildStore) advanceRebuildValidation(ctx context.Context, org, id string) error {
	initialized, err := s.initializeRebuildValidation(ctx, org, id)
	if err != nil || !initialized {
		return err
	}
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback(ctx)
	var shared bool
	if err = tx.QueryRow(ctx, `SELECT pg_try_advisory_xact_lock_shared($1)`, projectionRoutingLock).Scan(&shared); err != nil || !shared {
		return err
	}
	var previous []byte
	var cursor, corpusID, target string
	var scanned bool
	err = tx.QueryRow(ctx, `SELECT s.fingerprint,s.scan_cursor,s.scanned,s.corpus_id,o.target_generation_id FROM projection_rebuild_validation s
 JOIN operations o ON (o.organization,o.id)=(s.organization,s.operation_id)
 WHERE s.organization=$1 AND s.operation_id=$2 AND o.state='running' FOR UPDATE OF s`, org, id).Scan(&previous, &cursor, &scanned, &corpusID, &target)
	if errors.Is(err, pgx.ErrNoRows) {
		return operations.ErrNotRunning
	}
	if err != nil {
		return err
	}
	fingerprint, err := rebuildFingerprint(ctx, tx, org, id)
	if err != nil {
		return err
	}
	if !bytes.Equal(previous, fingerprint) {
		cursor, scanned = "", false
		if _, err = tx.Exec(ctx, `UPDATE projection_rebuild_validation SET owner_gap=false WHERE organization=$1 AND operation_id=$2`, org, id); err != nil {
			return err
		}
	}
	var activePlan string
	if err = tx.QueryRow(ctx, `SELECT COALESCE((SELECT plan_id FROM active_pipeline_plan),'')`).Scan(&activePlan); err != nil {
		return err
	}
	routing, err := planIngestionRouting(ctx, tx, activePlan)
	if err != nil {
		return err
	}
	expected, err := json.Marshal(routing)
	if err != nil {
		return err
	}
	var compatible bool
	err = tx.QueryRow(ctx, `SELECT t.ingestion_routing IS NOT NULL AND ($2::jsonb->>'default'='' OR (COALESCE(t.ingestion_routing->>'default','')=COALESCE($2::jsonb->>'default','') AND COALESCE(t.ingestion_routing->'routes','{}'::jsonb)=COALESCE($2::jsonb->'routes','{}'::jsonb))) FROM `+effectiveGenerationsSQL+` t WHERE t.id=$1`, target, expected).Scan(&compatible)
	if err != nil {
		return err
	}
	if !compatible {
		if _, err = tx.Exec(ctx, `UPDATE projection_rebuild_validation SET owner_gap=true,fingerprint=$3 WHERE organization=$1 AND operation_id=$2`, org, id, fingerprint); err != nil {
			return err
		}
		return tx.Commit(ctx)
	}
	if !scanned {
		rows, err := tx.Query(ctx, `SELECT id,current_version_id FROM records WHERE organization=$1 AND corpus_id=$2 AND current_version_id>$3 ORDER BY current_version_id LIMIT $4`, org, corpusID, cursor, rebuildValidationBatch)
		if err != nil {
			return err
		}
		type key struct{ record, version string }
		keys, err := pgx.CollectRows(rows, func(r pgx.CollectableRow) (key, error) {
			var k key
			err := r.Scan(&k.record, &k.version)
			return k, err
		})
		if err != nil {
			return err
		}
		ids := make([]string, len(keys))
		for i, k := range keys {
			ids[i] = k.record
			cursor = k.version
		}
		// Acquire observation rows before the fresh canonical read. Writers
		// arriving later recreate/increment a dirty row after these effects.
		if len(ids) > 0 {
			if _, err = tx.Exec(ctx, `INSERT INTO projection_rebuild_dirty_records(organization,operation_id,record_id)
 SELECT $1,$2,k FROM unnest($3::text[]) k ORDER BY k ON CONFLICT DO NOTHING`, org, id, ids); err != nil {
				return err
			}
			rows, err = tx.Query(ctx, `SELECT record_id FROM projection_rebuild_dirty_records WHERE organization=$1 AND operation_id=$2 AND record_id=ANY($3::text[]) ORDER BY record_id FOR UPDATE`, org, id, ids)
			if err != nil {
				return err
			}
			if _, err = pgx.CollectRows(rows, pgx.RowTo[string]); err != nil {
				return err
			}
			if err = s.checkRebuildRecords(ctx, tx, org, id, corpusID, target, expected, ids); err != nil {
				return err
			}
		}
		scanned = len(keys) < rebuildValidationBatch
	}
	// Only unchecked mutations need reconciliation. Checked rows represent
	// known gaps and return to this queue when coverage/eligibility changes.
	rows, err := tx.Query(ctx, `SELECT record_id FROM projection_rebuild_dirty_records WHERE organization=$1 AND operation_id=$2 AND NOT checked ORDER BY record_id LIMIT $3 FOR UPDATE`, org, id, rebuildValidationBatch)
	if err != nil {
		return err
	}
	ids, err := pgx.CollectRows(rows, pgx.RowTo[string])
	if err != nil {
		return err
	}
	if err = s.checkRebuildRecords(ctx, tx, org, id, corpusID, target, expected, ids); err != nil {
		return err
	}
	_, err = tx.Exec(ctx, `UPDATE projection_rebuild_validation SET fingerprint=$3,scan_cursor=$4,scanned=$5 WHERE organization=$1 AND operation_id=$2`, org, id, fingerprint, cursor, scanned)
	if err != nil {
		return err
	}
	return tx.Commit(ctx)
}

func (s RebuildStore) checkRebuildRecords(ctx context.Context, tx pgx.Tx, org, id, corpusID, target string, expected []byte, ids []string) error {
	if len(ids) == 0 {
		return nil
	}
	rows, err := tx.Query(ctx, `SELECT r.id,COALESCE(v.id,''),COALESCE((`+rebuildGapSQL+`),false),COALESCE((`+rebuildOwnerGapSQL+`),false)
 FROM unnest($5::text[]) k(record_id)
 JOIN LATERAL (SELECT * FROM records WHERE organization=$1 AND id=k.record_id LIMIT 1) r ON true
 LEFT JOIN LATERAL (SELECT * FROM record_versions WHERE organization=r.organization AND id=r.current_version_id LIMIT 1) v ON true`, org, corpusID, target, expected, ids)
	if err != nil {
		return err
	}
	checked, err := pgx.CollectRows(rows, func(r pgx.CollectableRow) (rebuildValidationRecord, error) {
		var out rebuildValidationRecord
		err := r.Scan(&out.record, &out.version, &out.gap, &out.ownerGap)
		return out, err
	})
	if err != nil {
		return err
	}
	// Rows disappeared from canonical state are clean; no foreign-key cascade
	// or mutable record lock is needed while owning their observation rows.
	gaps := make([]string, 0, len(checked))
	for _, r := range checked {
		if r.gap || r.ownerGap {
			gaps = append(gaps, r.record)
			if _, err = tx.Exec(ctx, `UPDATE projection_rebuild_dirty_records SET checked=true,version_id=$4,owner_gap=$5 WHERE organization=$1 AND operation_id=$2 AND record_id=$3`, org, id, r.record, r.version, r.ownerGap); err != nil {
				return err
			}
		}
	}

	_, err = tx.Exec(ctx, `DELETE FROM projection_rebuild_dirty_records WHERE organization=$1 AND operation_id=$2 AND record_id=ANY($3::text[]) AND NOT(record_id=ANY($4::text[]))`, org, id, ids, gaps)
	return err
}

// Select bounded ledger inputs before canonical checks. Forward ordering still
// honors the dispatch cursor, and an exhausted forward page wraps for repair.
func (s RebuildStore) rebuildValidationCandidates(ctx context.Context, org, id, after string, limit int) ([]retrieval.RebuildCandidate, error) {
	var corpusID, target string
	if err := s.Pool.QueryRow(ctx, `SELECT corpus_id,target_generation_id FROM operations WHERE organization=$1 AND id=$2`, org, id).Scan(&corpusID, &target); err != nil {
		return nil, err
	}
	query := `WITH page AS MATERIALIZED (SELECT record_id FROM projection_rebuild_dirty_records WHERE organization=$1 AND operation_id=$6 AND version_id>$5 ORDER BY version_id LIMIT $4)
 SELECT r.id,v.id,r.namespace,` + rebuildVectorsRequiredSQL + ` FROM page p JOIN records r ON r.organization=$1 AND r.id=p.record_id
 JOIN record_versions v ON (v.organization,v.id)=(r.organization,r.current_version_id) WHERE ` + rebuildGapSQL + ` ORDER BY v.id`
	rows, err := s.Pool.Query(ctx, query, org, corpusID, target, limit, after, id)
	if err != nil {
		return nil, err
	}
	return collectRebuildCandidates(rows)
}

// Dispatcher polling reclaims terminal scratch state even if its rebuild
// workflow has stopped. Each call owns one small batch and skips busy ledgers.
func (s OperationStore) cleanupRebuildValidation(parent context.Context) error {
	ctx, cancel := context.WithTimeout(parent, 100*time.Millisecond)
	defer cancel()
	tx, err := s.Pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback(ctx)
	// Drain writers that observed running before cancellation committed. Without
	// this fence their late UPSERT could recreate a ledger after its state was
	// removed, leaving an orphan that no dispatcher could discover.
	var acquired bool
	if err = tx.QueryRow(ctx, `SELECT pg_try_advisory_xact_lock($1)`, projectionRoutingLock).Scan(&acquired); err != nil || !acquired {
		return err
	}
	var org, id string
	err = tx.QueryRow(ctx, `SELECT s.organization,s.operation_id FROM projection_rebuild_validation s JOIN operations o ON (o.organization,o.id)=(s.organization,s.operation_id) WHERE o.state NOT IN ('queued','running') ORDER BY s.organization,s.operation_id LIMIT 1 FOR UPDATE OF s SKIP LOCKED`).Scan(&org, &id)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil
	}
	if err != nil {
		return err
	}
	_, err = tx.Exec(ctx, `WITH batch AS (SELECT record_id FROM projection_rebuild_dirty_records WHERE organization=$1 AND operation_id=$2 ORDER BY record_id LIMIT $3 FOR UPDATE SKIP LOCKED) DELETE FROM projection_rebuild_dirty_records d USING batch b WHERE d.organization=$1 AND d.operation_id=$2 AND d.record_id=b.record_id`, org, id, rebuildValidationBatch)
	if err != nil {
		return err
	}
	_, err = tx.Exec(ctx, `DELETE FROM projection_rebuild_validation s WHERE organization=$1 AND operation_id=$2 AND NOT COALESCE((SELECT true FROM projection_rebuild_dirty_records d WHERE d.organization=s.organization AND d.operation_id=s.operation_id ORDER BY d.record_id LIMIT 1),false)`, org, id)
	if err != nil {
		return err
	}
	return tx.Commit(ctx)
}
