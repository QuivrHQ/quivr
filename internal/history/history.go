// Package history runs bounded reclamation of expired operational detail.
// Identity and unfinished-work guards belong to the storage adapter.
package history

import (
	"context"
	"log/slog"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/lifecycle"
)

// Policy applies to the installation, never to an individual owner.
type Policy struct {
	ImportDetail, AlertDetail, Interval time.Duration
	Disabled                            bool
}

type Store interface {
	PruneHistory(context.Context, Policy, int) (int, error)
}

// Run admits one bounded pass per interval, including immediately on startup.
func Run(ctx context.Context, store Store, policy Policy) {
	if policy.Disabled {
		return
	}
	for ctx.Err() == nil {
		work, admitted := lifecycle.Admit(ctx)
		if !admitted {
			return
		}
		if _, err := store.PruneHistory(work, policy, 1000); err != nil && ctx.Err() == nil {
			slog.WarnContext(work, "history retention pass failed; retrying next interval", "error", err)
		}
		timer := time.NewTimer(policy.Interval)
		select {
		case <-ctx.Done():
			timer.Stop()
			return
		case <-timer.C:
		}
	}
}
