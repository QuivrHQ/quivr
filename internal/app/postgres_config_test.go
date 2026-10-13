package app

import (
	"encoding/json"
	"testing"
)

// Literal operator keys and the resulting driver config own pool sizing.
func TestPostgresPoolConfiguration(t *testing.T) {
	for _, tc := range []struct {
		input, dsn string
		timeout    string
		want       int32
		valid      bool
	}{
		{`{}`, "pool_max_conns=7", "30000", 7, true},
		{`{"postgres":{"max_connections":0}}`, "pool_max_conns=7", "30000", 7, true},
		{`{"postgres":{"max_connections":16}}`, "pool_max_conns=7", "30000", 16, true},
		{`{"postgres":{"max_connections":1}}`, "", "30000", 1, true},
		{`{"postgres":{"max_connections":-1}}`, "", "30000", 0, false},
		{`{"postgres":{"max_connections":2147483648}}`, "", "30000", 0, false},
		{`{"postgres":{"max_connections":2}}`, "pool_min_conns=3", "30000", 0, false},
		{`{"postgres":{"max_connections":2}}`, "pool_min_idle_conns=3", "30000", 0, false},
		{`{"postgres":{"transaction_timeout":"2s","max_connections":4}}`, "transaction_timeout=9000", "2000", 4, true},
		{`{"postgres":{"transaction_timeout":"0s"}}`, "", "", 0, false},
		{`{"postgres":{"transaction_timeout":"invalid"}}`, "", "", 0, false},
		{`{"postgres":{"transaction_timeout":"0.1ms"}}`, "", "", 0, false},
	} {
		var cfg Config
		err := json.Unmarshal([]byte(tc.input), &cfg)
		if err != nil {
			if tc.valid {
				t.Fatal(err)
			}
			continue
		}
		cfg.DatabaseURL = "host=localhost sslmode=disable " + tc.dsn
		got, err := cfg.poolConfig()
		if err == nil && got.ConnConfig.RuntimeParams["transaction_timeout"] != tc.timeout {
			t.Fatalf("transaction_timeout=%q, want %s ms", got.ConnConfig.RuntimeParams["transaction_timeout"], tc.timeout)
		}
		if (err == nil) != tc.valid || (tc.valid && got.MaxConns != tc.want) {
			t.Fatalf("config %s: got=%v err=%v want=%d valid=%v", tc.input, got, err, tc.want, tc.valid)
		}
	}
}
