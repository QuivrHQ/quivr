package postgres

import (
	"context"
	"testing"
	"time"
)

// Scrapes and the evaluation backlog log own a distinct storage-access contract:
// recounting source tables must not be required, even when those tables are busy.
// The transition owners verify each metric's units and admissibility separately.
func TestQueueMetricReadsUseMaintainedBacklog(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	pool := queueWorkPool(t, ctx)
	if err := Migrate(ctx, pool); err != nil {
		t.Fatal(err)
	}
	if _, err := (QueueSnapshots{Pool: pool}).Maintain(ctx); err != nil {
		t.Fatal(err)
	}
	tx, err := pool.Begin(ctx)
	if err != nil {
		t.Fatal(err)
	}
	defer tx.Rollback(ctx)
	if _, err = tx.Exec(ctx, `LOCK TABLE ingestion_receipts,evaluation_intents,deliveries,delivery_outbox IN ACCESS EXCLUSIVE MODE`); err != nil {
		t.Fatal(err)
	}
	for _, test := range []struct {
		name string
		read func(context.Context) (int64, error)
	}{
		{"ingestion", func(ctx context.Context) (int64, error) {
			n, _, err := (MaterializationStore{Pool: pool}).IngestionBacklog(ctx)
			return n, err
		}},
		{"evaluation", func(ctx context.Context) (int64, error) {
			b, err := (EvaluationStore{Pool: pool}).Backlog(ctx)
			return int64(b.Pending), err
		}},
		{"delivery", func(ctx context.Context) (int64, error) {
			b, err := (DeliveryStore{Pool: pool}).DeliveryBacklog(ctx)
			return int64(b.Pending), err
		}},
	} {
		t.Run(test.name, func(t *testing.T) {
			read, stop := context.WithTimeout(ctx, time.Second)
			defer stop()
			count, err := test.read(read)
			if err != nil || count != 0 {
				t.Fatalf("empty maintained %s backlog: count=%d error=%v; want zero without reading locked source storage", test.name, count, err)
			}
		})
	}
}
