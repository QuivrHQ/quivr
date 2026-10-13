package postgres_test

import (
	"context"
	"errors"
	"fmt"
	"testing"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/adapters/postgres"
	"github.com/The-Vibe-Company/quivr/internal/content"
	"github.com/The-Vibe-Company/quivr/internal/monitoring"
)

// The SQL evaluation owner protects checkpoint deferral, both dispatch modes,
// current subscription boundaries, and notice/delivery publication. Ordinary
// legacy evaluation tests cannot see committed canonical edits above the feed
// horizon. A real lower transaction deliberately stalls that horizon.
func TestParallelEvaluationWaitsForEditsAndPublishesNotices(t *testing.T) {
	for _, page := range []int{1, 32} {
		t.Run(fmt.Sprintf("page=%d", page), func(t *testing.T) {
			ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
			defer cancel()
			f := newCorrectionFixture(t, ctx, "adapter-parallel-evaluation-")
			subs := []monitoring.Subscription{f.subscribe("first"), f.subscribe("second")}
			journal := postgres.JournalStore{Pool: f.pool}
			if err := journal.SetParallel(ctx, true); err != nil {
				t.Fatal(err)
			}
			t.Cleanup(func() {
				if err := journal.SetParallel(context.Background(), false); err != nil {
					t.Error(err)
				}
			})
			record, version := f.publish("article", "first-version", "A neutral article")
			// Publish the original trigger, then stall a later Subscription edit.
			for range 2 {
				if _, err := journal.Advance(ctx); err != nil {
					t.Fatal(err)
				}
			}
			low, err := f.pool.Begin(ctx)
			if err != nil {
				t.Fatal(err)
			}
			defer low.Rollback(context.WithoutCancel(ctx))
			if _, err = low.Exec(ctx, `WITH writer AS MATERIALIZED (SELECT pg_current_xact_id() AS xid)
 INSERT INTO change_events(organization,sequence,event_id,corpus_id,event_type,resource_type,resource_id,writer_xid)
 SELECT $1,nextval('change_event_positions'),$2,$3,'record.accepted','record','other',writer.xid FROM writer`, f.org, content.StableID("event", f.org, "pending"), f.corpusID); err != nil {
				t.Fatal(err)
			}
			edited, err := f.service.CreateSubscriptionVersion(ctx, f.scope, subs[0].ID, monitoring.SubscriptionVersionInput{Key: "edit", SavedQueryVersionID: f.query.Current.VersionID, Evaluator: subs[0].Current.Evaluator, DestinationID: "dest"})
			if err != nil {
				t.Fatal(err)
			}
			evaluation := postgres.EvaluationStore{Pool: f.pool, Page: page}
			if _, err = evaluation.FanOut(ctx); err != nil {
				t.Fatal(err)
			}
			if n := f.count(`SELECT count(*) FROM evaluation_intents WHERE organization=$1`, f.org); n != 0 {
				t.Fatalf("dispatcher crossed unpublished edit: intents=%d", n)
			}
			if err = low.Commit(ctx); err != nil {
				t.Fatal(err)
			}
			for range 2 {
				if _, err = journal.Advance(ctx); err != nil {
					t.Fatal(err)
				}
			}
			if _, err = evaluation.FanOut(ctx); err != nil {
				t.Fatal(err)
			}
			// The trigger before the edit is evaluated by both original versions.
			if n := f.count(`SELECT count(*) FROM evaluation_intents WHERE organization=$1 AND record_version_id=$2 AND subscription_version_id=ANY($3::text[])`, f.org, version, []string{subs[0].Current.VersionID, subs[1].Current.VersionID}); n != 2 {
				t.Fatalf("edit lost earlier trigger: original intents=%d edited=%s", n, edited.VersionID)
			}
			if _, err = evaluation.FanOut(ctx); err != nil {
				t.Fatal(err)
			}
			if n := f.count(`SELECT count(*) FROM evaluation_intents WHERE organization=$1 AND record_version_id=$2`, f.org, version); n != 2 {
				t.Fatalf("repeat dispatch duplicated trigger: %d", n)
			}
			var sequence int64
			if err = f.pool.QueryRow(ctx, `SELECT sequence FROM evaluation_intents WHERE organization=$1 AND subscription_version_id=$2 AND record_version_id=$3`, f.org, subs[0].Current.VersionID, version).Scan(&sequence); err != nil {
				t.Fatal(err)
			}
			in := f.intent(subs[0], record, version)
			in.Sequence = sequence
			outcome, err := evaluation.CommitMatch(ctx, in, f.evidence(subs[0]))
			if err != nil || outcome != monitoring.OutcomeMatched {
				t.Fatalf("match=%s %v", outcome, err)
			}
			matchID := f.matchOf(subs[0], version)
			if _, err = f.store.Match(ctx, f.org, matchID); !errors.Is(err, monitoring.ErrNotFound) {
				t.Fatalf("unpublished Match became visible: %v", err)
			}
			works, err := (postgres.DeliveryStore{Pool: f.pool, Organization: f.org}).ClaimDeliveries(ctx, time.Minute, 1)
			if err != nil || len(works) != 1 {
				t.Fatalf("delivery claim=%+v %v", works, err)
			}
			if _, err = f.store.Delivery(ctx, f.org, works[0].DeliveryID); !errors.Is(err, monitoring.ErrNotFound) {
				t.Fatalf("unpublished Delivery became visible: %v", err)
			}
			delivery := postgres.DeliveryStore{Pool: f.pool, Organization: f.org}
			if _, _, err = delivery.Admit(ctx, works[0], time.Hour, func(string, string) bool { return true }); !errors.Is(err, postgres.ErrJournalUnpublished) {
				t.Fatalf("unpublished notice admitted: %v", err)
			}
			for range 2 {
				if _, err = journal.Advance(ctx); err != nil {
					t.Fatal(err)
				}
			}
			if m, err := f.store.Match(ctx, f.org, matchID); err != nil || m.RecordVersionID != version {
				t.Fatalf("published Match=%+v %v", m, err)
			}
			if d, err := f.store.Delivery(ctx, f.org, works[0].DeliveryID); err != nil || d.MatchID != matchID {
				t.Fatalf("published Delivery=%+v %v", d, err)
			}
			if _, reason, err := delivery.Admit(ctx, works[0], time.Hour, func(string, string) bool { return true }); err != nil || reason != "" {
				t.Fatalf("published delivery admission: %s %v", reason, err)
			}
		})
	}
}
