package app

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"time"

	"github.com/The-Vibe-Company/quivr/internal/adapters/postgres"
	"github.com/jackc/pgx/v5/pgxpool"
)

// runJournal is an offline operator command. It needs only PostgreSQL and
// requires an explicit acknowledgement before changing deployment-wide mode.
func runJournal(cfg Config, args []string, out io.Writer) error {
	if len(args) == 0 {
		return errors.New("usage: journal status|activate --previous-writers-retired|legacy --writers-drained|restored --writers-drained")
	}
	valid := len(args) == 1 && args[0] == "status"
	valid = valid || len(args) == 2 && ((args[0] == "activate" && args[1] == "--previous-writers-retired") || ((args[0] == "legacy" || args[0] == "restored") && args[1] == "--writers-drained"))
	if !valid {
		return errors.New("journal mode change requires its writer-drain acknowledgement")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	pc, err := cfg.poolConfig()
	if err != nil {
		return err
	}
	pool, err := pgxpool.NewWithConfig(ctx, pc)
	if err != nil {
		return errors.New("journal database unavailable")
	}
	defer pool.Close()
	if err = postgres.SchemaReady(ctx, pool); err != nil {
		return errors.New("journal schema is not ready")
	}
	journal := postgres.JournalStore{Pool: pool}
	switch args[0] {
	case "activate":
		err = journal.SetParallel(ctx, true)
	case "legacy":
		err = journal.SetParallel(ctx, false)
	case "restored":
		err = journal.ResetAfterRestore(ctx)
	}
	if err != nil {
		return errors.New("journal cutover failed; check queue initialization, writer drain and database availability")
	}
	status, err := journal.Status(ctx)
	if err != nil {
		return errors.New("journal status unavailable")
	}
	return json.NewEncoder(out).Encode(status)
}
