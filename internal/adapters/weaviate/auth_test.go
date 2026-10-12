package weaviate_test

import (
	"context"
	"crypto/tls"
	"io"
	"log"
	"net/http"
	"net/http/httptest"
	"sync/atomic"
	"testing"

	"github.com/The-Vibe-Company/quivr/internal/adapters/weaviate"
	"github.com/The-Vibe-Company/quivr/internal/outbound"
	"github.com/The-Vibe-Company/quivr/internal/testutil/tlsfixture"
)

// One wire owner covers authentication on ordinary and copied purge clients.
func TestIndexRequestsAuthenticateOnlyWhenConfigured(t *testing.T) {
	for _, tc := range []struct{ name, key, want string }{
		{"anonymous", "", ""}, {"authenticated", "fixture-index-key", "Bearer fixture-index-key"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			f := tlsfixture.New(t)
			var requests atomic.Int32
			server := httptest.NewUnstartedServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				requests.Add(1)
				if got := r.Header.Get("Authorization"); got != tc.want {
					t.Errorf("authorization header: got %q, want %q", got, tc.want)
				}
				switch r.URL.Path {
				case "/v1/.well-known/ready":
					w.WriteHeader(http.StatusNoContent)
				case "/v1/batch/objects":
					io.WriteString(w, `{"results":{"matches":0,"successful":0,"failed":0}}`)
				default:
					t.Errorf("unexpected path %s", r.URL.Path)
					w.WriteHeader(404)
				}
			}))
			server.Config.ErrorLog = log.New(io.Discard, "", 0)
			server.TLS = &tls.Config{Certificates: []tls.Certificate{f.Server}}
			server.StartTLS()
			defer server.Close()
			var keys []string
			if tc.key != "" {
				keys = []string{tc.key}
			}
			store, err := weaviate.NewWithTLS(server.URL, outbound.TLS{CAFile: f.CAFile, ServerName: "dependency.test"}, keys...)
			if err != nil {
				t.Fatal(err)
			}
			defer store.Client.CloseIdleConnections()
			if err = store.Ready(context.Background()); err != nil {
				t.Fatal(err)
			}
			if _, err = store.PurgeVersion(context.Background(), "QuivrTextV4", "org", "version"); err != nil {
				t.Fatal(err)
			}
			if requests.Load() != 2 {
				t.Fatalf("expected readiness and purge requests, got %d", requests.Load())
			}

			if tc.key == "" {
				return
			}

			var redirected atomic.Bool
			other := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) { redirected.Store(true) }))
			defer other.Close()
			redirect := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) { http.Redirect(w, r, other.URL, http.StatusFound) }))
			defer redirect.Close()
			// New also supports the same credential and redirect policy for local clients.
			if err = weaviate.New(redirect.URL, keys...).Ready(context.Background()); err == nil {
				t.Fatal("accepted a redirect to another dependency origin")
			}
			if redirected.Load() {
				t.Fatal("contacted redirect destination")
			}
		})
	}
}
