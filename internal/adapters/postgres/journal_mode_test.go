package postgres_test

import (
	"context"
	"fmt"
	"testing"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/adapters/postgres"
	"github.com/The-Vibe-Company/quivr/internal/content"
	"github.com/The-Vibe-Company/quivr/internal/corpus"
)

// The mode owner crosses both allocator cutovers through actual acceptance and
// feed cursors. Reinitializing a sequence beside live writers, or handing back
// an old legacy head, would reuse positions or lose the original traversal.
func TestJournalModeCutoverKeepsHistoricalPositionsAndReplay(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	pool := adapterPool(t, ctx)
	org := fmt.Sprintf("adapter-journal-mode-%d", time.Now().UnixNano())
	scope := corpus.Scope{Organization: org}
	c, _, err := (postgres.Store{Pool: pool}).Create(ctx, org, corpus.CreateInput{Key: "mode", Name: "Mode"})
	if err != nil {
		t.Fatal(err)
	}
	store := contentStores(pool)
	command := content.Command{Key: "legacy", Source: content.Source{CorpusID: c.ID, Namespace: "mode", RecordKey: "first"}, Content: content.Text{Kind: "text", Text: "first"}}
	receipt, err := store.Accept(ctx, scope, command)
	if err != nil {
		t.Fatal(err)
	}
	before, err := store.ReadChanges(ctx, org, c.ID, 0, 10, time.Hour)
	if err != nil || len(before.Events) != 2 {
		t.Fatalf("legacy=%+v err=%v", before, err)
	}
	journal := postgres.JournalStore{Pool: pool}
	if err = journal.SetParallel(ctx, true); err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = journal.SetParallel(context.Background(), false) })
	parallel := command
	parallel.Key = "parallel"
	parallel.Source.RecordKey = "second"
	if _, err = store.Accept(ctx, scope, parallel); err != nil {
		t.Fatal(err)
	}
	unpublished, err := store.ReadChanges(ctx, org, c.ID, before.Through, 10, time.Hour)
	if err != nil || len(unpublished.Events) != 0 {
		t.Fatalf("parallel write escaped safe head: %+v %v", unpublished, err)
	}
	if err = journal.SetParallel(ctx, false); err != nil {
		t.Fatal(err)
	}
	replay, err := store.Accept(ctx, scope, command)
	if err != nil || replay.ID != receipt.ID {
		t.Fatalf("old request changed across cutover: %+v %v", replay, err)
	}
	after, err := store.ReadChanges(ctx, org, c.ID, before.Through, 10, time.Hour)
	if err != nil || len(after.Events) != 2 || after.Events[0].Position <= before.Through {
		t.Fatalf("rollback traversal=%+v err=%v", after, err)
	}
	final := parallel
	final.Key = "after-reverse"
	final.Source.RecordKey = "third"
	if _, err = store.Accept(ctx, scope, final); err != nil {
		t.Fatal(err)
	}
	resumed, err := store.ReadChanges(ctx, org, c.ID, after.Through, 10, time.Hour)
	if err != nil || len(resumed.Events) != 2 || resumed.Events[0].Position <= after.Through {
		t.Fatalf("reversed allocator reused positions: %+v %v", resumed, err)
	}
	original, err := store.ReadChanges(ctx, org, c.ID, 0, 10, time.Hour)
	if err != nil || len(original.Events) != 6 || original.Events[0].ID != before.Events[0].ID || original.Events[0].Position != before.Events[0].Position {
		t.Fatalf("historical identity changed: %+v %v", original, err)
	}
}
