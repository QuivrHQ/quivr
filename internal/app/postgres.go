package app

import (
	"github.com/The-Vibe-Company/quivr/internal/adapters/postgres"
	"github.com/jackc/pgx/v5/pgxpool"
	"strconv"
	"time"
)

// PostgresConfig bounds connections per process, independent of worker slots.
type PostgresConfig struct {
	MaxConnections     int32  `json:"max_connections"`
	TransactionTimeout string `json:"transaction_timeout"`
}

func (cfg Config) poolConfig() (*pgxpool.Config, error) {
	if cfg.Postgres.MaxConnections < 0 {
		return nil, badConfig(configInvalid, "postgres.max_connections", "postgres.max_connections must be positive, or zero for URL/driver sizing")
	}
	pool, err := postgres.PoolConfig(cfg.DatabaseURL, cfg.TLS.Postgres)
	if err != nil {
		return nil, invalidConfig("database_url", "invalid database_url or PostgreSQL TLS settings", err)
	}
	if limit := cfg.Postgres.MaxConnections; limit > 0 {
		if pool.MinConns > limit || pool.MinIdleConns > limit {
			return nil, badConfig(configConflict, "postgres.max_connections", "postgres.max_connections is smaller than the URL's minimum pool size")
		}
		pool.MaxConns = limit
	}
	timeout := 30 * time.Second
	if cfg.Postgres.TransactionTimeout != "" {
		timeout, err = time.ParseDuration(cfg.Postgres.TransactionTimeout)
		if err != nil || timeout.Milliseconds() < 1 || timeout.Milliseconds() > 2147483647 {
			return nil, badConfig(configInvalid, "postgres.transaction_timeout", "postgres.transaction_timeout must be a positive duration in PostgreSQL's millisecond range")
		}
	}
	// Bound all engine transactions, including read-only snapshots, from BEGIN.
	// A transaction-local SET after allocating an event cannot bound the time
	// already spent in its transaction. PostgreSQL 17 enforces this at the server.
	pool.ConnConfig.RuntimeParams["transaction_timeout"] = strconv.FormatInt(timeout.Milliseconds(), 10)
	return pool, nil
}
