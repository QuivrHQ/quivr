package postgres_test

import (
	"context"
	"errors"
	"fmt"
	"testing"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/adapters/postgres"
	"github.com/The-Vibe-Company/quivr/internal/audit"
	"github.com/The-Vibe-Company/quivr/internal/content"
	"github.com/The-Vibe-Company/quivr/internal/corpus"
	"github.com/jackc/pgx/v5/pgxpool"
)

// Concurrent audited acceptance owns request convergence, no speculative
// identity leak, per-Record ordering and A/B/A-prime lineage. The earlier
// sequential correction owners cannot expose a second identity inserted while
// the same request's first transaction is still invisible.
func TestParallelRequestClaimsKeepRecordOrderAndCorrectionLineage(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	pool := adapterPool(t, ctx)
	org := fmt.Sprintf("adapter-parallel-requests-%d", time.Now().UnixNano())
	scope := corpus.Scope{Organization: org}
	c, _, err := (postgres.Store{Pool: pool}).Create(ctx, org, corpus.CreateInput{Key: "requests", Name: "Requests"})
	if err != nil {
		t.Fatal(err)
	}
	journal := postgres.JournalStore{Pool: pool}
	if err = journal.SetParallel(ctx, true); err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		if err := journal.SetParallel(context.Background(), false); err != nil {
			t.Error(err)
		}
	})
	store := contentStores(pool)
	a := content.Command{Key: "a", Source: content.Source{CorpusID: c.ID, Namespace: "requests", RecordKey: "article"}, Position: "1", Content: content.Text{Kind: "text", Text: "A"}}
	accepted := make(chan content.Receipt, 1)
	firstDone := make(chan error, 1)
	release := make(chan struct{})
	go func() {
		event := audit.Event{Action: "receipt.accept", TargetType: "record", Organization: org, Outcome: "accepted"}
		firstDone <- (postgres.AuditStore{Pool: pool}).Record(ctx, &event, func(work context.Context) error {
			receipt, err := store.Accept(work, scope, a)
			if err != nil {
				return err
			}
			event.TargetID = receipt.RecordID
			accepted <- receipt
			select {
			case <-release:
				return nil
			case <-ctx.Done():
				return ctx.Err()
			}
		})
	}()
	var first content.Receipt
	select {
	case first = <-accepted:
	case err := <-firstDone:
		t.Fatalf("first audited acceptance: %v", err)
	case <-ctx.Done():
		t.Fatal(ctx.Err())
	}
	cfg := pool.Config()
	cfg.MaxConns = 3
	cfg.ConnConfig.RuntimeParams["application_name"] = org
	competing, err := pgxpool.NewWithConfig(ctx, cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer competing.Close()
	writer := postgres.SubmissionStore{Pool: competing}
	b := a
	b.Key = "b"
	b.Position = "2"
	b.Content.Text = "B"
	type result struct {
		receipt content.Receipt
		err     error
	}
	secondDone := make(chan result, 1)
	conflictDone := make(chan result, 1)
	duplicateDone := make(chan result, 1)
	go func() { r, e := writer.Accept(ctx, scope, b); secondDone <- result{r, e} }()
	changed := a
	changed.Source.RecordKey = "other-identity"
	go func() { r, e := writer.Accept(ctx, scope, changed); conflictDone <- result{r, e} }()
	go func() { r, e := writer.Accept(ctx, scope, a); duplicateDone <- result{r, e} }()
	// Observe all competitors waiting on real database locks, not elapsed time.
	for {
		var waiting int
		if err = pool.QueryRow(ctx, `SELECT count(*) FROM pg_stat_activity WHERE application_name=$1 AND wait_event_type='Lock'`, org).Scan(&waiting); err != nil {
			t.Fatal(err)
		}
		if waiting == 3 {
			break
		}
		select {
		case r := <-secondDone:
			t.Fatalf("same Record escaped open predecessor: %+v", r)
		case r := <-conflictDone:
			t.Fatalf("same key escaped open request: %+v", r)
		case r := <-duplicateDone:
			t.Fatalf("duplicate escaped open request: %+v", r)
		default:
		}
	}
	for range 2 {
		if _, err = journal.Advance(ctx); err != nil {
			t.Fatal(err)
		}
	}
	hidden, err := store.ReadChanges(ctx, org, c.ID, 0, 10, time.Hour)
	if err != nil || len(hidden.Events) != 0 {
		t.Fatalf("audited uncommitted facts leaked: %+v %v", hidden, err)
	}
	close(release)
	if err = <-firstDone; err != nil {
		t.Fatal(err)
	}
	second := <-secondDone
	if second.err != nil {
		t.Fatal(second.err)
	}
	conflicting := <-conflictDone
	if !errors.Is(conflicting.err, content.ErrConflict) {
		t.Fatalf("changed bytes under same request: %+v", conflicting)
	}
	duplicate := <-duplicateDone
	if duplicate.err != nil || duplicate.receipt.ID != first.ID || duplicate.receipt.NewRevision {
		t.Fatalf("concurrent duplicate=%+v", duplicate)
	}
	replay, err := store.Accept(ctx, scope, a)
	if err != nil || replay.ID != first.ID || replay.NewRevision {
		t.Fatalf("request replay=%+v %v", replay, err)
	}
	aprime := a
	aprime.Key = "a-prime"
	aprime.Position = "3"
	last, err := store.Accept(ctx, scope, aprime)
	if err != nil {
		t.Fatal(err)
	}
	wa, _, err := store.Work(ctx, org, first.ID)
	if err != nil {
		t.Fatal(err)
	}
	wb, _, err := store.Work(ctx, org, second.receipt.ID)
	if err != nil {
		t.Fatal(err)
	}
	wp, _, err := store.Work(ctx, org, last.ID)
	if err != nil {
		t.Fatal(err)
	}
	if wa.Order != 1 || wb.Order != 2 || wp.Order != 3 || wp.VersionID == wa.VersionID || wp.PredecessorID != wb.VersionID {
		t.Fatalf("lineage A=%+v B=%+v A-prime=%+v", wa, wb, wp)
	}
	for range 3 {
		if _, err = journal.Advance(ctx); err != nil {
			t.Fatal(err)
		}
	}
	feed, err := store.ReadChanges(ctx, org, c.ID, 0, 10, time.Hour)
	if err != nil {
		t.Fatal(err)
	}
	want := []string{first.ID, second.receipt.ID, last.ID}
	seen := 0
	for _, e := range feed.Events {
		if e.Type != "record.accepted" {
			continue
		}
		if seen >= len(want) || e.ID != content.StableID("event", org, "record.accepted", "record", want[seen]) {
			t.Fatalf("per-Record order changed: %+v want receipts %v", feed, want)
		}
		seen++
	}
	var records int
	if err = pool.QueryRow(ctx, `SELECT count(*) FROM records WHERE organization=$1`, org).Scan(&records); err != nil {
		t.Fatal(err)
	}
	if seen != 3 || records != 1 {
		t.Fatalf("request facts missing or speculative identity leaked: events=%d Records=%d", seen, records)
	}
}
