package app

import (
	"github.com/The-Vibe-Company/quivr/internal/history"
	"time"
)

type HistoryRetentionConfig struct {
	ImportDetail string `json:"import_detail"`
	AlertDetail  string `json:"alert_detail"`
	Interval     string `json:"interval"`
	Disabled     bool   `json:"disabled"`
}

func (c HistoryRetentionConfig) parse() (history.Policy, error) {
	p := history.Policy{ImportDetail: 720 * time.Hour, AlertDetail: 720 * time.Hour, Interval: time.Hour, Disabled: c.Disabled}
	for _, item := range []struct {
		key, value string
		target     *time.Duration
	}{
		{"history_retention.import_detail", c.ImportDetail, &p.ImportDetail},
		{"history_retention.alert_detail", c.AlertDetail, &p.AlertDetail},
		{"history_retention.interval", c.Interval, &p.Interval},
	} {
		if item.value == "" {
			continue
		}
		d, err := time.ParseDuration(item.value)
		if err != nil || d <= 0 {
			return history.Policy{}, badConfig(configInvalid, item.key, "history_retention durations must be positive Go durations")
		}
		*item.target = d
	}
	return p, nil
}
