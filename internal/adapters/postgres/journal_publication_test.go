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

// The feed owns prefix completeness. Real open transactions expose missing
// rows, aborted gaps and XID/sequence inversion; visible maxima cannot prove a
// prefix. The two low events also test atomic multi-event publication.
func TestParallelJournalDoesNotPublishPastAnOpenLowerPosition(t *testing.T) {
	for _, scenario := range []struct {
		name                string
		rollback, olderHigh bool
	}{{name: "late commit"}, {name: "rollback gap", rollback: true}, {name: "older xid higher sequence", olderHigh: true}} {
		t.Run(scenario.name, func(t *testing.T) {
			ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
			defer cancel()
			pool := adapterPool(t, ctx)
			org := fmt.Sprintf("adapter-safe-prefix-%d", time.Now().UnixNano())
			c, _, err := (postgres.Store{Pool: pool}).Create(ctx, org, corpus.CreateInput{Key: "prefix", Name: "Prefix"})
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
			high, err := pool.Begin(ctx)
			if err != nil {
				t.Fatal(err)
			}
			defer high.Rollback(context.WithoutCancel(ctx))
			if scenario.olderHigh {
				if _, err = high.Exec(ctx, `SELECT pg_current_xact_id()`); err != nil {
					t.Fatal(err)
				}
			}
			low, err := pool.Begin(ctx)
			if err != nil {
				t.Fatal(err)
			}
			defer low.Rollback(context.WithoutCancel(ctx))
			appendSQL := `WITH writer AS MATERIALIZED (SELECT pg_current_xact_id() AS xid)
 INSERT INTO change_events(organization,sequence,event_id,corpus_id,event_type,resource_type,resource_id,writer_xid)
 SELECT $1,nextval('change_event_positions'),$2,$3,'record.accepted','record',$4,writer.xid FROM writer RETURNING sequence`
			var lowPosition, secondPosition, highPosition int64
			if err = low.QueryRow(ctx, appendSQL, org, content.StableID("event", org, "low"), c.ID, "late-one").Scan(&lowPosition); err != nil {
				t.Fatal(err)
			}
			if err = low.QueryRow(ctx, appendSQL, org, content.StableID("event", org, "second"), c.ID, "late-two").Scan(&secondPosition); err != nil {
				t.Fatal(err)
			}
			if err = high.QueryRow(ctx, appendSQL, org, content.StableID("event", org, "high"), c.ID, "early").Scan(&highPosition); err != nil {
				t.Fatal(err)
			}
			if err = high.Commit(ctx); err != nil {
				t.Fatal(err)
			}
			// A crashed sampler can leave an unobserved sequence gap. It is never
			// recovery evidence by itself, and must not starve the oldest valid sample.
			if _, err = pool.Exec(ctx, `SELECT nextval('change_event_positions')`); err != nil {
				t.Fatal(err)
			}
			for range 3 {
				if _, err = journal.Advance(ctx); err != nil {
					t.Fatal(err)
				}
			}
			feed := postgres.ChangeStore{Pool: pool}
			w, err := feed.ReadChanges(ctx, org, c.ID, 0, 10, time.Hour)
			if err != nil || w.Head >= lowPosition || len(w.Events) != 0 {
				t.Fatalf("crossed open event %d: %+v %v", lowPosition, w, err)
			}
			if scenario.rollback {
				err = low.Rollback(ctx)
			} else {
				err = low.Commit(ctx)
			}
			if err != nil {
				t.Fatal(err)
			}
			if _, err = journal.Advance(ctx); err != nil {
				t.Fatal(err)
			}
			w, err = feed.ReadChanges(ctx, org, c.ID, w.Through, 10, time.Hour)
			want := []int64{lowPosition, secondPosition, highPosition}
			if scenario.rollback {
				want = want[2:]
			}
			if err != nil || len(w.Events) != len(want) {
				t.Fatalf("late traversal: %+v %v; want positions %v", w, err, want)
			}
			for i, event := range w.Events {
				if event.Position != want[i] {
					t.Fatalf("position[%d]=%d want %d", i, event.Position, want[i])
				}
			}
			continued, err := feed.ReadChanges(ctx, org, c.ID, w.Through, 10, time.Hour)
			if err != nil || len(continued.Events) != 0 {
				t.Fatalf("cursor repeated events: %+v %v", continued, err)
			}
		})
	}
}
