package postgres_test

import (
	"context"
	"errors"
	"fmt"
	"testing"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/adapters/postgres"
	"github.com/The-Vibe-Company/quivr/internal/changes"
	"github.com/The-Vibe-Company/quivr/internal/content"
	"github.com/The-Vibe-Company/quivr/internal/corpus"
)

// TestChangeFeedStartExcludesVisibleBacklogAndKeepsInFlightRows owns the
// exact start-now contract at the SQL boundary. The old row is committed but
// remains above the published head when the start snapshot is captured; the
// lower writer is still open at that snapshot. A safe-head-only reader would
// replay the old row, while a max-visible reader would skip the lower writer.
func TestChangeFeedStartExcludesVisibleBacklogAndKeepsInFlightRows(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	pool := adapterPool(t, ctx)
	org := fmt.Sprintf("adapter-feed-start-%d", time.Now().UnixNano())
	corpora := corpus.Service{Store: postgres.Store{Pool: pool}}
	scope := corpus.Scope{Organization: org, Actions: []string{"corpora:write", "changes:read"}, Corpora: []string{"*"}}
	c, _, err := corpora.Create(ctx, scope, corpus.CreateInput{Key: "feed", Name: "Feed"})
	if err != nil {
		t.Fatal(err)
	}

	var oldParallel bool
	var oldPublished, oldSampled int64
	var oldSampleXID *string
	if err = pool.QueryRow(ctx, `SELECT parallel,published_through,sampled_through,sample_xid::text FROM change_journal_publication WHERE singleton`).Scan(&oldParallel, &oldPublished, &oldSampled, &oldSampleXID); err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		_, _ = pool.Exec(context.Background(), `UPDATE change_journal_publication SET parallel=$1,published_through=$2,sampled_through=$3,sample_xid=$4::xid8 WHERE singleton`, oldParallel, oldPublished, oldSampled, oldSampleXID)
	})

	var sequence int64
	if err = pool.QueryRow(ctx, `SELECT COALESCE((SELECT CASE WHEN is_called THEN last_value ELSE last_value-1 END FROM change_event_positions),0)`).Scan(&sequence); err != nil {
		t.Fatal(err)
	}
	base := sequence + 1_000_000
	if _, err = pool.Exec(ctx, `SELECT setval('change_event_positions',$1,true)`, base); err != nil {
		t.Fatal(err)
	}
	if _, err = pool.Exec(ctx, `UPDATE change_journal_publication SET parallel=true,published_through=0,sampled_through=0,sample_xid=NULL WHERE singleton`); err != nil {
		t.Fatal(err)
	}

	// This committed row is deliberately left unpublished until after the
	// start snapshot. Its writer xid is visible in that snapshot and must be
	// excluded even though publication later advances over it.
	if _, err = pool.Exec(ctx, `WITH writer AS MATERIALIZED (SELECT pg_current_xact_id() AS xid)
INSERT INTO change_events(organization,sequence,event_id,corpus_id,event_type,resource_type,resource_id,writer_xid)
SELECT $1,nextval('change_event_positions'),$2,$3,'record.accepted','record','visible-before-start',writer.xid FROM writer`, org, content.StableID("event", org, "visible-before-start"), c.ID); err != nil {
		t.Fatal(err)
	}
	if _, err = pool.Exec(ctx, `UPDATE change_events SET occurred_at=clock_timestamp()-interval '2 hours' WHERE organization=$1 AND resource_id='visible-before-start'`, org); err != nil {
		t.Fatal(err)
	}

	lower, err := pool.Begin(ctx)
	if err != nil {
		t.Fatal(err)
	}
	defer lower.Rollback(context.WithoutCancel(ctx))
	var lowerPosition int64
	if err = lower.QueryRow(ctx, `WITH writer AS MATERIALIZED (SELECT pg_current_xact_id() AS xid)
INSERT INTO change_events(organization,sequence,event_id,corpus_id,event_type,resource_type,resource_id,writer_xid)
SELECT $1,nextval('change_event_positions'),$2,$3,'record.accepted','record','in-flight-at-start',writer.xid FROM writer RETURNING sequence`, org, content.StableID("event", org, "in-flight-at-start"), c.ID).Scan(&lowerPosition); err != nil {
		t.Fatal(err)
	}

	feed := postgres.ChangeStore{Pool: pool}
	start, err := feed.StartChanges(ctx, org, c.ID, time.Hour)
	if err != nil {
		t.Fatal(err)
	}
	if start.Position != 0 || start.StartID == "" {
		t.Fatalf("start=%+v, want unpublished head and a snapshot reference", start)
	}
	if err = lower.Commit(ctx); err != nil {
		t.Fatal(err)
	}
	if _, err = pool.Exec(ctx, `UPDATE change_journal_publication SET published_through=$1,sampled_through=$1,sample_xid=NULL WHERE singleton`, lowerPosition); err != nil {
		t.Fatal(err)
	}

	w, err := feed.ReadChangesResume(ctx, org, c.ID, start, 10, time.Hour)
	if err != nil {
		t.Fatal(err)
	}
	if w.Expired || len(w.Events) != 1 || w.Events[0].ResourceID != "in-flight-at-start" {
		t.Fatalf("exact start window=%+v, want only the in-flight row", w)
	}
	if w.Resume.StartID != "" || w.Resume.Position != lowerPosition {
		t.Fatalf("completed ceiling must retire snapshot state: window resume=%+v ceiling=%d", w.Resume, w.StartCeiling)
	}

	missing, err := feed.ReadChangesResume(ctx, org, c.ID, changes.Resume{Position: lowerPosition, StartID: start.StartID + "missing"}, 10, time.Hour)
	if err != nil {
		t.Fatal(err)
	}
	if !missing.Expired {
		t.Fatalf("missing start reference must expire: %+v", missing)
	}
	if _, err = feed.ReadChangesResume(ctx, org, "another-corpus", start, 10, time.Hour); !errors.Is(err, changes.ErrCursorScope) {
		t.Fatalf("start reused for another Corpus: %v", err)
	}

	// The start row remains a pruning pin until publication passes its captured
	// ceiling. At the ceiling, the old row is still retained for the exact
	// start; once the safe head advances past it, aged rows become deletable.
	if _, err = pool.Exec(ctx, `UPDATE change_events SET occurred_at=clock_timestamp()-interval '2 hours' WHERE organization=$1`, org); err != nil {
		t.Fatal(err)
	}
	var before int64
	if err = pool.QueryRow(ctx, `SELECT count(*) FROM change_events WHERE organization=$1`, org).Scan(&before); err != nil {
		t.Fatal(err)
	}
	if deleted, err := feed.PruneChanges(ctx, time.Hour, []string{org}, 4, 1); err != nil || deleted != 0 {
		t.Fatalf("live start pin allowed pruning at its ceiling: deleted=%d err=%v", deleted, err)
	}
	if _, err = pool.Exec(ctx, `UPDATE change_journal_publication SET published_through=$1,sampled_through=$1 WHERE singleton`, lowerPosition+1); err != nil {
		t.Fatal(err)
	}
	deleted, err := feed.PruneChanges(ctx, time.Hour, []string{org}, 4, 1)
	if err != nil || deleted == 0 {
		t.Fatalf("expired start pin did not release aged rows: deleted=%d err=%v", deleted, err)
	}
	var after int64
	if err = pool.QueryRow(ctx, `SELECT count(*) FROM change_events WHERE organization=$1`, org).Scan(&after); err != nil {
		t.Fatal(err)
	}
	if after >= before {
		t.Fatalf("prune released after safe head passed ceiling: before=%d after=%d", before, after)
	}
	// Snapshot start references are retention state, not permanent facts.
	if _, err = pool.Exec(ctx, `UPDATE change_feed_starts SET expires_at=clock_timestamp()-interval '1 second' WHERE id=$1`, start.StartID); err != nil {
		t.Fatal(err)
	}
	if _, err = feed.PruneChanges(ctx, time.Hour, []string{org}, 4, 1); err != nil {
		t.Fatal(err)
	}
	var remaining int
	if err = pool.QueryRow(ctx, `SELECT count(*) FROM change_feed_starts WHERE id=$1`, start.StartID).Scan(&remaining); err != nil || remaining != 0 {
		t.Fatalf("expired start retained: %d %v", remaining, err)
	}

}
