// Measure acceptance through its real SQL boundary on an empty loopback
// database. It calls no providers and reports relative evidence, not a CI gate.
package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"net/url"
	"os"
	"sort"
	"strings"
	"sync"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/adapters/postgres"
	"github.com/The-Vibe-Company/quivr/internal/app"
	"github.com/The-Vibe-Company/quivr/internal/content"
	"github.com/The-Vibe-Company/quivr/internal/corpus"
	"github.com/jackc/pgx/v5/pgxpool"
)

type trial struct {
	Mode                    string  `json:"mode"`
	Concurrency             int     `json:"concurrency"`
	Accepted                int     `json:"accepted"`
	Errors                  int     `json:"errors"`
	Seconds                 float64 `json:"seconds"`
	ItemsPerSecond          float64 `json:"accepted_items_per_second"`
	P50MS                   float64 `json:"latency_p50_ms"`
	P95MS                   float64 `json:"latency_p95_ms"`
	LockWaitSamples         int64   `json:"lock_wait_samples"`
	MaxUnpublishedPositions int64   `json:"max_unpublished_positions"`
	MaxPendingAgeSeconds    float64 `json:"max_pending_age_seconds"`
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "parallel acceptance measurement failed:", err)
		os.Exit(1)
	}
}
func run() error {
	config := flag.String("config", "", "operator JSON for an empty loopback parallel_measure database")
	items := flag.Int("items", 512, "fixed accepted items per trial (1..10000)")
	flag.Parse()
	if *items < 1 || *items > 10000 {
		return fmt.Errorf("items must be in 1..10000")
	}
	data, err := os.ReadFile(*config)
	if err != nil {
		return fmt.Errorf("read operator configuration")
	}
	var cfg app.Config
	if err = json.Unmarshal(data, &cfg); err != nil {
		return fmt.Errorf("decode operator configuration")
	}
	u, err := url.Parse(cfg.DatabaseURL)
	if err != nil {
		return fmt.Errorf("invalid local database URL")
	}
	if u.Hostname() != "127.0.0.1" && u.Hostname() != "localhost" && u.Hostname() != "::1" {
		return fmt.Errorf("measurement requires loopback PostgreSQL")
	}
	if !strings.HasPrefix(strings.TrimPrefix(u.Path, "/"), "parallel_measure_") {
		return fmt.Errorf("measurement requires an empty parallel_measure_ database")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()
	pc, err := postgres.PoolConfig(cfg.DatabaseURL, cfg.TLS.Postgres)
	if err != nil {
		return fmt.Errorf("database configuration")
	}
	pc.MaxConns = 40
	pc.ConnConfig.RuntimeParams["synchronous_commit"] = "on"
	pc.ConnConfig.RuntimeParams["transaction_timeout"] = "30s"
	pc.ConnConfig.RuntimeParams["application_name"] = "parallel-journal-acceptance"
	pool, err := pgxpool.NewWithConfig(ctx, pc)
	if err != nil {
		return fmt.Errorf("open database")
	}
	defer pool.Close()
	var empty bool
	if err = pool.QueryRow(ctx, `SELECT NOT EXISTS(SELECT FROM pg_tables WHERE schemaname='public')`).Scan(&empty); err != nil || !empty {
		return fmt.Errorf("database must be empty")
	}
	if err = app.BootstrapDatabase(ctx, pool, nil); err != nil {
		return fmt.Errorf("database bootstrap")
	}
	queues := postgres.QueueSnapshots{Pool: pool}
	for {
		more, err := queues.Maintain(ctx)
		if err != nil {
			return fmt.Errorf("queue bootstrap")
		}
		if !more {
			break
		}
	}
	// Open the same number of connections before every mode, outside timing.
	warm := make([]*pgxpool.Conn, 0, 40)
	for range 40 {
		c, err := pool.Acquire(ctx)
		if err != nil {
			return fmt.Errorf("warm pool")
		}
		warm = append(warm, c)
	}
	for _, c := range warm {
		c.Release()
	}
	journal := postgres.JournalStore{Pool: pool}
	var version string
	if err = pool.QueryRow(ctx, `SHOW server_version`).Scan(&version); err != nil {
		return fmt.Errorf("database version")
	}
	results := []trial{}
	for _, parallel := range []bool{false, true} {
		if err = journal.SetParallel(ctx, parallel); err != nil {
			return fmt.Errorf("mode cutover")
		}
		for _, workers := range []int{1, 8, 32} {
			r, err := measure(ctx, pool, journal, parallel, workers, *items)
			if err != nil {
				return err
			}
			results = append(results, r)
		}
	}
	if err = journal.SetParallel(ctx, false); err != nil {
		return fmt.Errorf("measurement drain")
	}
	return json.NewEncoder(os.Stdout).Encode(map[string]any{"postgres": version, "synchronous_commit": "on", "connections": 40, "items_per_trial": *items, "boundary": "SubmissionStore.Accept; no providers", "evidence": "local relative comparison of candidate legacy/parallel modes; not a merge gate", "trials": results})
}

func measure(parent context.Context, pool *pgxpool.Pool, journal postgres.JournalStore, parallel bool, workers, items int) (trial, error) {
	ctx, cancel := context.WithTimeout(parent, time.Minute)
	defer cancel()
	mode := "legacy"
	if parallel {
		mode = "parallel"
	}
	r := trial{Mode: mode, Concurrency: workers}
	org := fmt.Sprintf("parallel-measure-%s-%d-%d", mode, workers, time.Now().UnixNano())
	c, _, err := (postgres.Store{Pool: pool}).Create(ctx, org, corpus.CreateInput{Key: "acceptance", Name: "Acceptance"})
	if err != nil {
		return r, fmt.Errorf("create measurement scope")
	}
	scope := corpus.Scope{Organization: org}
	observeCtx, stop := context.WithCancel(ctx)
	observed := make(chan trial, 1)
	go func() {
		samples := trial{}
		timer := time.NewTicker(10 * time.Millisecond)
		defer timer.Stop()
		for {
			select {
			case <-observeCtx.Done():
				observed <- samples
				return
			case <-timer.C:
				var waiting int64
				if err := pool.QueryRow(observeCtx, `SELECT count(*) FROM pg_stat_activity WHERE application_name='parallel-journal-acceptance' AND wait_event_type='Lock'`).Scan(&waiting); err == nil {
					samples.LockWaitSamples += waiting
				}
				if status, err := journal.Status(observeCtx); err == nil {
					samples.MaxUnpublishedPositions = max(samples.MaxUnpublishedPositions, status.UnpublishedPositions)
					samples.MaxPendingAgeSeconds = max(samples.MaxPendingAgeSeconds, status.PendingAgeSeconds)
				}
			}
		}
	}()
	pubCtx, stopPublisher := context.WithCancel(ctx)
	published := make(chan struct{})
	go func() { defer close(published); journal.Run(pubCtx) }()
	// Queue maintenance runs at the engine's one-second cadence outside producers.
	queueCtx, stopQueue := context.WithCancel(ctx)
	maintained := make(chan struct{})
	go func() {
		defer close(maintained)
		timer := time.NewTicker(time.Second)
		defer timer.Stop()
		for {
			select {
			case <-queueCtx.Done():
				return
			case <-timer.C:
				_, _ = (postgres.QueueSnapshots{Pool: pool}).Maintain(queueCtx)
			}
		}
	}()
	jobs := make(chan int, items)
	for i := range items {
		jobs <- i
	}
	close(jobs)
	type answer struct {
		latency float64
		err     error
	}
	answers := make(chan answer, items)
	start := time.Now()
	var wg sync.WaitGroup
	for range workers {
		wg.Add(1)
		go func() {
			defer wg.Done()
			store := postgres.SubmissionStore{Pool: pool}
			for i := range jobs {
				key := fmt.Sprint(i)
				at := time.Now()
				_, err := store.Accept(ctx, scope, content.Command{Key: key, Source: content.Source{CorpusID: c.ID, Namespace: "measurement", RecordKey: key}, Content: content.Text{Kind: "text", Text: "A neutral document for acceptance throughput."}})
				answers <- answer{float64(time.Since(at).Microseconds()) / 1000, err}
			}
		}()
	}
	wg.Wait()
	r.Seconds = time.Since(start).Seconds()
	close(answers)
	latencies := make([]float64, 0, items)
	for a := range answers {
		latencies = append(latencies, a.latency)
		if a.err == nil {
			r.Accepted++
		} else {
			r.Errors++
		}
	}
	stop()
	samples := <-observed
	stopPublisher()
	<-published
	stopQueue()
	<-maintained
	r.LockWaitSamples = samples.LockWaitSamples
	r.MaxUnpublishedPositions = samples.MaxUnpublishedPositions
	r.MaxPendingAgeSeconds = samples.MaxPendingAgeSeconds
	sort.Float64s(latencies)
	r.P50MS = latencies[(len(latencies)-1)*50/100]
	r.P95MS = latencies[(len(latencies)-1)*95/100]
	r.ItemsPerSecond = float64(r.Accepted) / r.Seconds
	if r.Errors != 0 {
		return r, fmt.Errorf("acceptance returned %d errors in %s concurrency %d", r.Errors, mode, workers)
	}
	return r, nil
}
