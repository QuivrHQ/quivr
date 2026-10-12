package postgres_test

import (
	"context"
	"encoding/json"
	"errors"
	"testing"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/adapters/postgres"
	"github.com/The-Vibe-Company/quivr/internal/app"
	"github.com/The-Vibe-Company/quivr/internal/content"
	"github.com/The-Vibe-Company/quivr/internal/history"
	"github.com/The-Vibe-Company/quivr/internal/monitoring"
)

// Owns reclamation at the real storage boundary: expired detail disappears,
// while replay identities, feed references and unanswered work remain usable.
// Tiny batches and fresh adapters exercise durable progress without clock waits.
func TestHistoryRetentionPreservesReplayAndUnansweredWork(t *testing.T) {
	ctx, cancel := context.WithTimeout(t.Context(), 30*time.Second)
	defer cancel()
	pool := scratchDatabase(t, ctx)
	if err := app.BootstrapDatabase(ctx, pool, app.Config{}.DeploymentSpaces(nil)); err != nil {
		t.Fatal(err)
	}
	if err := postgres.EnsureIndexes(ctx, pool); err != nil {
		t.Fatal(err)
	}
	f := newDeliveryFixture(t, ctx, pool, "retention-", 3)
	exec := func(sql string, args ...any) {
		t.Helper()
		if _, err := pool.Exec(ctx, sql, args...); err != nil {
			t.Fatal(err)
		}
	}
	exec(`UPDATE delivery_outbox SET available_at='infinity' WHERE organization=$1`, f.org)
	ack, refused := f.admit(f.deliveries[0], time.Hour, f.configured)
	if refused != "" {
		t.Fatal(refused)
	}
	if err := f.ds.Record(ctx, ack, monitoring.AttemptOutcome{Outcome: monitoring.AttemptAcknowledged, HTTPStatus: 204}, monitoring.Retry{Window: time.Hour}); err != nil {
		t.Fatal(err)
	}
	exec(`INSERT INTO delivery_attempts(organization,id,delivery_id,number) SELECT $1,'retained-attempt-'||n,$2,n FROM generate_series(2,4) n`, f.org, ack.DeliveryID)
	exhausted, refused := f.admit(f.deliveries[1], time.Hour, f.configured)
	if refused != "" {
		t.Fatal(refused)
	}
	if err := f.ds.Record(ctx, exhausted, monitoring.AttemptOutcome{Outcome: monitoring.AttemptPermanentError, HTTPStatus: 400}, monitoring.Retry{Window: time.Hour}); err != nil {
		t.Fatal(err)
	}
	// Old creation time alone must never expire a newly acknowledged Delivery.
	exec(`UPDATE deliveries SET created_at=now()-interval '90 days' WHERE organization=$1`, f.org)
	exec(`INSERT INTO monitoring_notices(organization,event_id,kind,match_id,record_id,record_version_id,subscription_id,subscription_version_id,delivery_id,previous_match_id,body,position)
 SELECT organization,'pull-notice',kind,match_id,record_id,record_version_id,subscription_id,subscription_version_id,NULL,previous_match_id,body,position
 FROM monitoring_notices WHERE organization=$1 LIMIT 1`, f.org)

	exec(`UPDATE ingestion_receipts SET accepted_at=now()-interval '90 days',canonical_request='retained audit bytes',command='{"detail":"retained"}' WHERE organization=$1`, f.org)
	cmd := content.Command{Key: "hit", Source: content.Source{CorpusID: f.corpusID, Namespace: "delivery", RecordKey: "hit"}, Content: content.Text{Kind: "text", Text: "Dépêche hit"}}
	canonical, err := json.Marshal(cmd)
	if err != nil {
		t.Fatal(err)
	}
	exec(`UPDATE ingestion_receipts SET request_digest=NULL,canonical_request=$2 WHERE organization=$1 AND request_key='hit'`, f.org, canonical)
	pendingCommand := content.Command{Key: "pending", Source: content.Source{CorpusID: f.corpusID, Namespace: "history", RecordKey: "pending"}, Content: content.Text{Kind: "text", Text: "Unfinished import"}}
	pendingReceipt, err := f.contents.Accept(ctx, f.scope, pendingCommand)
	if err != nil {
		t.Fatal(err)
	}
	exec(`UPDATE ingestion_receipts SET accepted_at=now()-interval '90 days',command='{"detail":"unfinished"}',canonical_request='unfinished bytes' WHERE organization=$1 AND id=$2`, f.org, pendingReceipt.ID)
	// Historical Versions share real blob references but are no longer current
	// or desired. A pending receipt and quarantine independently protect detail.
	for _, id := range []string{"retired", "guarded", "quarantined"} {
		exec(`INSERT INTO record_versions(organization,id,record_id,slot,digest,acceptance_order,source_position,text_blob_id,manifest_blob_id,provenance,processing,quarantined)
 SELECT organization,$2,record_id,$2,digest,acceptance_order,source_position,text_blob_id,manifest_blob_id,provenance,'idle',$2='quarantined'
 FROM record_versions WHERE organization=$1 LIMIT 1`, f.org, id)
		exec(`INSERT INTO accepted_revisions(organization,record_id,slot,digest,version_id,acceptance_order,source_position,command,accepted_at)
 SELECT organization,record_id,slot,digest,id,acceptance_order,source_position,'{"detail":"retained"}',now()-interval '90 days'
 FROM record_versions WHERE organization=$1 AND id=$2`, f.org, id)
	}
	exec(`UPDATE accepted_revisions SET command='{"detail":"retained"}',accepted_at=now()-interval '90 days' WHERE organization=$1`, f.org)
	exec(`INSERT INTO ingestion_receipts(organization,id,request_key,canonical_request,command,corpus_id,record_id,acceptance_order,slot,digest,version_id)
 SELECT organization,'guarded-receipt','guarded-receipt','pending bytes','{"detail":"pending"}',corpus_id,record_id,acceptance_order+100,'guarded',digest,'guarded'
 FROM ingestion_receipts WHERE organization=$1 AND request_key='hit'`, f.org)
	exec(`INSERT INTO monitoring_checkpoints(organization,position) VALUES($1,10000)`, f.org)
	for i, version := range []string{"retired", "guarded", "guarded", "quarantined"} {
		state := "done"
		if i == 2 {
			state = "pending"
		}
		exec(`INSERT INTO evaluation_intents(organization,subscription_version_id,sequence,subscription_id,corpus_id,record_id,record_version_id,state,outcome,retention_started_at)
 SELECT m.organization,m.subscription_version_id,$2,m.subscription_id,m.corpus_id,m.record_id,$3,$4,'no_match',now()-interval '90 days'
 FROM matches m WHERE m.organization=$1 AND m.subscription_id=$5`, f.org, i+1, version, state, f.subs[0].ID)
	}
	exec(`INSERT INTO evaluation_intents(organization,subscription_version_id,sequence,subscription_id,corpus_id,record_id,record_version_id,state,outcome,retention_started_at)
 SELECT organization,subscription_version_id,5,subscription_id,corpus_id,record_id,record_version_id,'done','not_ready',now()-interval '90 days'
 FROM matches WHERE organization=$1 AND subscription_id=$2`, f.org, f.subs[0].ID)
	exec(`INSERT INTO evaluation_intents(organization,subscription_version_id,sequence,subscription_id,corpus_id,record_id,record_version_id,state,outcome,retention_started_at)
 SELECT organization,subscription_version_id,n,subscription_id,corpus_id,record_id,'retired','done',CASE WHEN n=6 THEN 'duplicate' ELSE 'ineligible' END,now()-interval '90 days'
 FROM matches CROSS JOIN generate_series(6,7) n WHERE organization=$1 AND subscription_id=$2`, f.org, f.subs[0].ID)
	policy := history.Policy{ImportDetail: 720 * time.Hour, AlertDetail: 720 * time.Hour, Interval: time.Hour}
	prune := func() {
		t.Helper()
		if _, err := (postgres.HistoryStore{Pool: pool}).PruneHistory(ctx, policy, 1); err != nil {
			t.Fatal(err)
		}
	}
	prune()
	if n := f.count(`SELECT count(*) FROM matches WHERE organization=$1 AND retention_started_at IS NOT NULL`, f.org); n != 1 {
		t.Fatalf("clock initialization exceeded one candidate: %d", n)
	}
	for range 16 {
		prune()
	}
	if n := f.count(`SELECT count(*) FROM matches WHERE organization=$1 AND retention_started_at IS NULL`, f.org); n != 0 {
		t.Fatalf("restart lost conservative clocks: %d", n)
	}
	if n := f.count(`SELECT count(*) FROM monitoring_notices WHERE organization=$1 AND event_id='pull-notice' AND octet_length(body)>0 AND retention_started_at IS NOT NULL`, f.org); n != 1 {
		t.Fatal("new pull-notice clock must preserve its full window")
	}
	if f.attempts(ack.DeliveryID) != 4 {
		t.Fatal("recent acknowledgement history was removed")
	}
	if n := f.count(`SELECT count(*) FROM ingestion_receipts WHERE organization=$1 AND state='resolved' AND (octet_length(canonical_request)>0 OR command<>'{}')`, f.org); n != 0 {
		t.Fatalf("expired receipt payloads=%d", n)
	}
	if n := f.count(`SELECT count(*) FROM accepted_revisions WHERE organization=$1 AND command='{}'`, f.org); n != 1 {
		t.Fatalf("only retired revision detail should expire: %d", n)
	}
	if n := f.count(`SELECT count(*) FROM evaluation_intents WHERE organization=$1`, f.org); n != 5 {
		t.Fatalf("current/pending/quarantined evaluations and earliest paid decision must remain: %d", n)
	}
	if n := f.count(`SELECT count(*) FROM ingestion_receipts WHERE organization=$1 AND id=$2 AND command<>'{}'`, f.org, pendingReceipt.ID); n != 1 {
		t.Fatal("unfinished receipt detail expired")
	}
	// Replay, changed-envelope rejection and connector unchanged-item skips
	// still work after the full canonical copy was reclaimed.
	r, err := f.contents.Accept(ctx, f.scope, cmd)
	if err != nil {
		t.Fatal(err)
	}
	if found, err := (postgres.ReceiptStore{Pool: pool}).HasReceipt(ctx, f.org, cmd.Key); err != nil || !found {
		t.Fatalf("connector replay identity: %v %v", found, err)
	}
	cmd.Content.Text = "Changed envelope"
	if _, err = f.contents.Accept(ctx, f.scope, cmd); !errors.Is(err, content.ErrConflict) {
		t.Fatalf("compacted replay conflict=%v", err)
	}
	if r.State != "resolved" {
		t.Fatalf("compacted receipt=%+v", r)
	}
	// Before the feed is pruned, aged evidence and pull-only notice bytes stay.
	exec(`UPDATE matches SET retention_started_at=now()-interval '90 days' WHERE organization=$1`, f.org)
	exec(`UPDATE monitoring_notices SET retention_started_at=now()-interval '90 days' WHERE organization=$1`, f.org)
	for range 8 {
		prune()
	}
	if m, err := f.service.Matches(ctx, f.scope, f.subs[0].ID, 0, 10); err != nil || len(m) != 1 || m[0].Evidence.Explanation != "fixture" {
		t.Fatalf("unpruned evidence=%+v %v", m, err)
	}
	if n := f.count(`SELECT count(*) FROM monitoring_notices WHERE organization=$1 AND event_id='pull-notice' AND octet_length(body)>0`, f.org); n != 1 {
		t.Fatal("unpruned pull-notice body expired")
	}
	// Append-only attempt/outcome guards have no application retention path.
	// Keep acknowledged parents and delivery-backed bodies intact as well.
	exec(`DELETE FROM change_events WHERE organization=$1`, f.org)
	exec(`INSERT INTO change_journal_prunes(organization,pruned_through) VALUES($1,10000)`, f.org)
	for range 12 {
		prune()
	}
	if d := f.read(ack.DeliveryID); d.State != "delivered" || len(d.Event) == 0 || f.attempts(d.ID) != 4 {
		t.Fatalf("append-only acknowledged history lost=%+v", d)
	}
	if n := f.count(`SELECT count(*) FROM monitoring_notices WHERE organization=$1 AND event_id='pull-notice' AND octet_length(body)=0`, f.org); n != 1 {
		t.Fatal("expired pull-only notice body retained")
	}
	if d := f.read(f.deliveries[2]); d.State != "pending" || len(d.Event) == 0 {
		t.Fatalf("unanswered notice lost=%+v", d)
	}
	if d := f.read(exhausted.DeliveryID); d.State != "exhausted" || f.attempts(d.ID) != 1 {
		t.Fatalf("manual retry history lost=%+v", d)
	}
	// The compact Match still arbitrates duplicates; the public read refuses
	// expired evidence rather than manufacturing a changed successful response.
	matches, err := f.service.Matches(ctx, f.scope, f.subs[0].ID, 0, 10)
	if !errors.Is(err, monitoring.ErrEvidenceExpired) {
		t.Fatalf("expired match history=%+v %v", matches, err)
	}
	if m, err := f.service.Matches(ctx, f.scope, f.subs[1].ID, 0, 10); err != nil || len(m) != 1 || m[0].Evidence.Explanation != "fixture" {
		t.Fatalf("pending delivery evidence=%+v %v", m, err)
	}
	if n := f.count(`SELECT count(*) FROM monitoring_notices WHERE organization=$1`, f.org); n != 4 {
		t.Fatalf("deduplication notices=%d", n)
	}
	intent := monitoring.Intent{Organization: f.org, SubscriptionID: f.subs[0].ID, SubscriptionVersionID: f.subs[0].Current.VersionID,
		Sequence: 20000, CorpusID: f.corpusID, RecordID: r.RecordID, VersionID: r.VersionID}
	evaluations := postgres.EvaluationStore{Pool: pool}
	// Enrichment committed before a correction can still be waiting behind the
	// dispatch checkpoint. Retention must keep the pair's decided identity.
	exec(`INSERT INTO change_events(organization,sequence,event_id,corpus_id,event_type,resource_type,resource_id,record_version_id)
 VALUES($1,11000,$1||'-late-enrichment',$2,'record.enrichment_available','record',$3,'retired')`, f.org, f.corpusID, r.RecordID)
	exec(`UPDATE organization_journals SET last_sequence=11000 WHERE organization=$1`, f.org)
	if _, err := evaluations.FanOut(ctx); err != nil {
		t.Fatal(err)
	}
	if n := f.count(`SELECT count(*) FROM evaluation_intents WHERE organization=$1 AND subscription_version_id=$2 AND record_version_id='retired' AND state='pending'`, f.org, f.subs[0].Current.VersionID); n != 0 {
		t.Fatal("retention reopened paid evaluation from undispatched enrichment")
	}
	retired := intent
	retired.VersionID, retired.Sequence = "retired", 11000
	if target, err := evaluations.Target(ctx, retired); err != nil || !target.Decided {
		t.Fatalf("retained pair decision must suppress future paid calls: %+v %v", target, err)
	}
	if outcome, err := evaluations.CommitMatch(ctx, intent, monitoring.MatchEvidence{Evaluator: f.subs[0].Current.Evaluator, Explanation: "repeated"}); err != nil || outcome != monitoring.OutcomeDuplicate {
		t.Fatalf("compacted identity did not prevent duplicate alert: %s %v", outcome, err)
	}
	if _, err := f.contents.Withdraw(ctx, f.scope, content.Withdrawal{Key: "withdraw-hit", Source: cmd.Source}); err != nil {
		t.Fatal(err)
	}
	intent.Kind = monitoring.IntentWithdrawal
	if outcome, err := evaluations.CommitWithdrawal(ctx, intent); err != nil || outcome != monitoring.OutcomeWithdrawalNotified {
		t.Fatalf("compacted Match lost withdrawal reference: %s %v", outcome, err)
	}
	if outcome, err := evaluations.CommitWithdrawal(ctx, intent); err != nil || outcome != monitoring.OutcomeDuplicate {
		t.Fatalf("withdrawal notice identity lost: %s %v", outcome, err)
	}
	if _, err := pool.Exec(ctx, `DELETE FROM delivery_attempts WHERE organization=$1`, f.org); err == nil {
		t.Fatal("ordinary attempt deletion was allowed")
	}
}
