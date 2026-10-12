package app

import (
	"encoding/json"
	"testing"
	"time"
)

// Owns the external installation keys and omitted-key defaults. A rename or
// invalid duration must be rejected before any worker can reclaim history.
func TestHistoryRetentionConfiguration(t *testing.T) {
	for _, tc := range []struct {
		input                     string
		imports, alerts, interval time.Duration
		disabled, invalid         bool
	}{
		{`{}`, 720 * time.Hour, 720 * time.Hour, time.Hour, false, false},
		{`{"history_retention":{"import_detail":"48h","alert_detail":"96h","interval":"5m","disabled":true}}`, 48 * time.Hour, 96 * time.Hour, 5 * time.Minute, true, false},
		{`{"history_retention":{"import_detail":"0s"}}`, 0, 0, 0, false, true},
		{`{"history_retention":{"alert_detail":"-1h"}}`, 0, 0, 0, false, true},
		{`{"history_retention":{"interval":"tomorrow"}}`, 0, 0, 0, false, true},
	} {
		var cfg Config
		if err := json.Unmarshal([]byte(tc.input), &cfg); err != nil {
			t.Fatal(err)
		}
		p, err := cfg.HistoryRetention.parse()
		if (err != nil) != tc.invalid {
			t.Fatalf("%s: policy=%+v error=%v", tc.input, p, err)
		}
		if !tc.invalid && (p.ImportDetail != tc.imports || p.AlertDetail != tc.alerts || p.Interval != tc.interval || p.Disabled != tc.disabled) {
			t.Fatalf("%s: policy=%+v", tc.input, p)
		}
	}
}
