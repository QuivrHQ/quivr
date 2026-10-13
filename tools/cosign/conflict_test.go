package cosign_test

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"errors"
	"testing"

	"github.com/go-openapi/strfmt"
	protobundle "github.com/sigstore/protobuf-specs/gen/pb-go/bundle/v1"
	"github.com/sigstore/rekor/pkg/generated/client/entries"
	"github.com/sigstore/rekor/pkg/generated/models"
	"github.com/sigstore/sigstore-go/pkg/sign"
)

// The dependency owns conflict recovery. Exercise its real signer/log boundary
// with the same signed content and Rekor's existing-entry response contract.
func TestRekorExistingEntry(t *testing.T) {
	ctx := context.Background()
	key, err := sign.NewEphemeralKeypair(nil)
	if err != nil {
		t.Fatal(err)
	}
	content := sign.DSSEData{Data: []byte("immutable image digest"), PayloadType: "application/vnd.in-toto+json"}
	signature, digest, err := key.SignData(ctx, content.PreAuthEncoding())
	if err != nil {
		t.Fatal(err)
	}
	pub, err := key.GetPublicKeyPem()
	if err != nil {
		t.Fatal(err)
	}

	for _, tc := range []struct {
		name      string
		conflict  bool
		postError bool
		getError  bool
		invalid   bool
		wantError bool
	}{
		{name: "created"},
		{name: "existing", conflict: true},
		{name: "other upload error", postError: true, wantError: true},
		{name: "existing entry unavailable", conflict: true, getError: true, wantError: true},
		{name: "malformed existing evidence", conflict: true, invalid: true, wantError: true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			bundle := &protobundle.Bundle{VerificationMaterial: &protobundle.VerificationMaterial{}}
			content.Bundle(bundle, signature, digest, key.GetHashAlgorithm())
			client := &rekorResponse{conflict: tc.conflict, postError: tc.postError, getError: tc.getError, invalid: tc.invalid}
			log := sign.NewRekor(&sign.RekorOptions{Client: client})
			err := log.GetTransparencyLogEntry(ctx, []byte(pub), bundle)
			if (err != nil) != tc.wantError {
				t.Fatalf("expected error=%v, got %v", tc.wantError, err)
			}
			if tc.wantError {
				if len(bundle.VerificationMaterial.TlogEntries) != 0 {
					t.Fatal("failed upload/fetch must not produce log evidence")
				}
				return
			}
			if tc.conflict && !client.fetched {
				t.Fatal("existing entry must be fetched")
			}
			evidence := bundle.VerificationMaterial.TlogEntries
			if len(evidence) != 1 || evidence[0].LogIndex != 7 || evidence[0].IntegratedTime != 1700000000 {
				t.Fatalf("missing existing entry evidence: %v", evidence)
			}
			if string(evidence[0].CanonicalizedBody) != string(client.body) || evidence[0].InclusionProof.TreeSize != 8 {
				t.Fatal("existing entry body and inclusion proof were not preserved")
			}
		})
	}
}

type rekorResponse struct {
	conflict, postError, getError, invalid, fetched bool
	body                                            []byte
	entry                                           models.LogEntryAnon
}

func (r *rekorResponse) CreateLogEntry(params *entries.CreateLogEntryParams, _ ...entries.ClientOption) (*entries.CreateLogEntryCreated, error) {
	if r.postError {
		return nil, errors.New("upload unavailable")
	}
	body, err := json.Marshal(params.ProposedEntry)
	if err != nil {
		return nil, err
	}
	r.body = body
	index, timestamp, size := int64(7), int64(1700000000), int64(8)
	logID, root, checkpoint := "aabb", "ccdd", "checkpoint"
	if r.invalid {
		logID = "invalid hex"
	}
	r.entry = models.LogEntryAnon{
		Body: base64.StdEncoding.EncodeToString(body), LogIndex: &index, IntegratedTime: &timestamp, LogID: &logID,
		Verification: &models.LogEntryAnonVerification{InclusionProof: &models.InclusionProof{
			LogIndex: &index, TreeSize: &size, RootHash: &root, Checkpoint: &checkpoint,
		}},
	}
	if r.conflict {
		return nil, &entries.CreateLogEntryConflict{Location: strfmt.URI("https://rekor.example.invalid/api/v1/log/entries/existing-uuid")}
	}
	return &entries.CreateLogEntryCreated{ETag: "existing-uuid", Payload: models.LogEntry{"existing-uuid": r.entry}}, nil
}

func (r *rekorResponse) GetLogEntryByUUID(params *entries.GetLogEntryByUUIDParams, _ ...entries.ClientOption) (*entries.GetLogEntryByUUIDOK, error) {
	r.fetched = true
	if params.EntryUUID != "existing-uuid" {
		return nil, errors.New("wrong existing entry requested")
	}
	if r.getError {
		return nil, errors.New("existing entry unavailable")
	}
	return &entries.GetLogEntryByUUIDOK{Payload: models.LogEntry{"existing-uuid": r.entry}}, nil
}
