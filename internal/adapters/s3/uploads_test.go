package s3_test

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"net/http/httputil"
	"net/url"
	"os"
	"sync/atomic"
	"testing"
	"time"

	store "github.com/The-Vibe-Company/quivr/internal/adapters/s3"
	"github.com/The-Vibe-Company/quivr/internal/uploads"
)

func transferConfig(t *testing.T) store.Config {
	t.Helper()
	path := os.Getenv("QUIVR_ADAPTER_CONFIG")
	if path == "" {
		t.Skip("real S3 adapter suite runs inside make verify")
	}
	data, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	var cfg struct {
		S3 store.Config `json:"s3"`
	}
	if err = json.Unmarshal(data, &cfg); err != nil {
		t.Fatal(err)
	}
	return cfg.S3
}

func TestPresignedTransferVerifiesAndReadsSignedReference(t *testing.T) {
	cfg := transferConfig(t)
	blobs := store.New(cfg)
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
	defer cancel()
	objectKey := "adapter-transfers/upload-object"
	data := []byte("Ligne un\nLigne deux\n")
	sum := sha256.Sum256(data)
	digest := hex.EncodeToString(sum[:])

	url, headers, err := blobs.PresignPut(ctx, objectKey, int64(len(data)), digest, "text/plain", time.Minute)
	if err != nil {
		t.Fatal(err)
	}
	request, err := http.NewRequestWithContext(ctx, http.MethodPut, url, bytes.NewReader(data))
	if err != nil {
		t.Fatal(err)
	}
	for name, value := range headers {
		request.Header.Set(name, value)
	}
	response, err := (&http.Client{Timeout: 15 * time.Second}).Do(request)
	if err != nil {
		t.Fatal(err)
	}
	_, _ = io.Copy(io.Discard, response.Body)
	response.Body.Close()
	if response.StatusCode/100 != 2 {
		t.Fatalf("presigned transfer refused: %d", response.StatusCode)
	}
	if err = blobs.Verify(ctx, objectKey, int64(len(data)), digest); err != nil {
		t.Fatalf("transferred bytes did not verify: %v", err)
	}
	other := sha256.Sum256([]byte("different expectation"))
	if err = blobs.Verify(ctx, objectKey, int64(len(data)), hex.EncodeToString(other[:])); !errors.Is(err, uploads.ErrVerificationMismatch) {
		t.Fatal("altered expectation was not reported as a mismatch")
	}
	if err = blobs.Verify(ctx, "adapter-transfers/absent", int64(len(data)), digest); err == nil {
		t.Fatal("absent object verified")
	}
	// A signed GET reference reads exactly the stored bytes without credentials.
	signed, expires, err := blobs.PresignGet(ctx, objectKey, time.Minute)
	if err != nil || !expires.After(time.Now()) {
		t.Fatalf("signed reference: %v", err)
	}
	got, err := http.Get(signed)
	if err != nil {
		t.Fatal(err)
	}
	body, _ := io.ReadAll(got.Body)
	got.Body.Close()
	if got.StatusCode != 200 || !bytes.Equal(body, data) {
		t.Fatalf("signed GET returned %d %q", got.StatusCode, body)
	}
}

// A connector attachment reaches storage only through a grant: a presigned PUT
// pinned to its length, checksum and media type. Bytes other than the
// granted ones never verify, whether storage refuses them or not, and a
// granted object larger than the 2 MiB canonical-object read bound verifies
// without reading its payload when the store exposes the upload checksum.
func TestGrantedUploadsVerifyOnlyTheGrantedBytes(t *testing.T) {
	cfg := transferConfig(t)
	target, err := url.Parse(cfg.Endpoint)
	if err != nil {
		t.Fatal(err)
	}
	proxy := httputil.NewSingleHostReverseProxy(target)
	var gets, heads atomic.Int32
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodGet {
			gets.Add(1)
		}
		if r.Method == http.MethodHead {
			heads.Add(1)
		}
		proxy.ServeHTTP(w, r)
	}))
	defer server.Close()
	cfg.Endpoint = server.URL
	blobs := store.New(cfg)
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()
	data := bytes.Repeat([]byte("pièce jointe "), 300_000)
	sum := sha256.Sum256(data)
	digest := hex.EncodeToString(sum[:])
	put := func(objectKey string, body []byte) int {
		t.Helper()
		url, headers, err := blobs.PresignPut(ctx, objectKey, int64(len(data)), digest, "application/pdf", time.Minute)
		if err != nil {
			t.Fatal(err)
		}
		request, _ := http.NewRequestWithContext(ctx, http.MethodPut, url, bytes.NewReader(body))
		for name, value := range headers {
			request.Header.Set(name, value)
		}
		request.ContentLength = int64(len(body))
		response, err := (&http.Client{Timeout: 30 * time.Second}).Do(request)
		if err != nil {
			t.Fatal(err)
		}
		defer response.Body.Close()
		_, _ = io.Copy(io.Discard, response.Body)
		return response.StatusCode
	}
	granted := "adapter-transfers/granted-" + digest
	if status := put(granted, data); status/100 != 2 {
		t.Fatalf("valid upload: HTTP %d", status)
	}
	if err := blobs.Verify(ctx, granted, int64(len(data)), digest); err != nil {
		t.Fatalf("granted bytes did not verify: %v", err)
	}
	altered := bytes.Clone(data)
	altered[0] = 'P'
	other := "adapter-transfers/altered-" + digest
	if status := put(other, altered); status != http.StatusBadRequest {
		t.Fatalf("corrupted upload: HTTP %d, want 400 BadDigest", status)
	}
	if err := blobs.Verify(ctx, other, int64(len(data)), digest); err == nil {
		t.Fatal("bytes other than the granted ones verified")
	}
	// A page of successfully uploaded items must not reread payloads to verify.
	gets.Store(0)
	heads.Store(0)
	for i := 0; i < 32; i++ {
		key := fmt.Sprintf("adapter-transfers/page-%d-%s", i, digest)
		if status := put(key, data); status/100 != 2 {
			t.Fatalf("page item %d upload: HTTP %d", i, status)
		}
		if err := blobs.Verify(ctx, key, int64(len(data)), digest); err != nil {
			t.Fatalf("page item %d: %v", i, err)
		}
	}
	if got := gets.Load(); got != 0 {
		t.Fatalf("page verification performed %d payload GETs, want zero", got)
	}
	if got := heads.Load(); got != 32 {
		t.Fatalf("page verification performed %d HEADs, want 32", got)
	}
}

// The wire boundary owns compatibility with checksum-less stores and objects,
// and keeps mismatches terminal while storage failures remain retryable.
func TestTransferVerificationChecksumCompatibility(t *testing.T) {
	data := []byte("uploaded bytes")
	sum := sha256.Sum256(data)
	digest := hex.EncodeToString(sum[:])
	checksum := base64.StdEncoding.EncodeToString(sum[:])
	for _, tc := range []struct {
		name, checksum, checksumType string
		headStatus                   int
		headSize                     int
		body                         []byte
		gets                         int32
		mismatch, unavailable        bool
	}{
		{name: "checksum", checksum: checksum, headSize: len(data), body: data},
		{name: "wrong checksum", checksum: base64.StdEncoding.EncodeToString(make([]byte, 32)), headSize: len(data), body: data, mismatch: true},
		{name: "malformed checksum", checksum: "invalid", headSize: len(data), body: data, mismatch: true},
		{name: "wrong size", checksum: checksum, headSize: len(data) + 1, body: data, mismatch: true},
		{name: "legacy object", headSize: len(data), body: data, gets: 1},
		{name: "legacy corrupt object", headSize: len(data), body: []byte("altered bytes!"), gets: 1, mismatch: true},
		{name: "legacy oversized object", headSize: len(data), body: append(bytes.Clone(data), '!'), gets: 1, mismatch: true},
		{name: "composite checksum", checksum: checksum + "-1", checksumType: "COMPOSITE", headSize: len(data), body: data, gets: 1},
		{name: "checksum mode unsupported", headStatus: 400, body: data, gets: 1},
		{name: "HEAD unsupported", headStatus: 405, body: data, gets: 1},
		{name: "HEAD not implemented", headStatus: 501, body: data, gets: 1},
		{name: "missing", headStatus: 404, unavailable: true},
		{name: "access denied", headStatus: 403, unavailable: true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			var gets, heads atomic.Int32
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				switch r.Method {
				case http.MethodHead:
					heads.Add(1)
					if r.Header.Get("X-Amz-Checksum-Mode") != "ENABLED" {
						t.Error("HEAD omitted checksum mode")
					}
					if tc.headStatus != 0 {
						w.WriteHeader(tc.headStatus)
						return
					}
					w.Header().Set("Content-Length", fmt.Sprint(tc.headSize))
					if tc.checksum != "" {
						w.Header().Set("X-Amz-Checksum-Sha256", tc.checksum)
					}
					if tc.checksumType != "" {
						w.Header().Set("X-Amz-Checksum-Type", tc.checksumType)
					}
				case http.MethodGet:
					gets.Add(1)
					w.Write(tc.body)
				default:
					t.Errorf("unexpected method %s", r.Method)
					w.WriteHeader(405)
				}
			}))
			defer server.Close()
			blobs := store.New(store.Config{Endpoint: server.URL, AccessKey: "local-test", SecretKey: "local-test", Bucket: "uploads"})
			err := blobs.Verify(context.Background(), "object", int64(len(data)), digest)
			if errors.Is(err, uploads.ErrVerificationMismatch) != tc.mismatch {
				t.Fatalf("verification error %v, want mismatch=%v", err, tc.mismatch)
			}
			if tc.unavailable && err == nil {
				t.Fatal("unavailable storage verified")
			}
			if !tc.unavailable && !tc.mismatch && err != nil {
				t.Fatal(err)
			}
			if got := gets.Load(); got != tc.gets {
				t.Fatalf("payload GETs=%d, want %d", got, tc.gets)
			}
			if got := heads.Load(); got != 1 {
				t.Fatalf("HEADs=%d, want 1", got)
			}
		})
	}
}
