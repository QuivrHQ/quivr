#!/usr/bin/env bash
# Until an official Cosign release includes Rekor-v1 conflict recovery, build
# v3.1.3 with sigstore-go v1.3.0 (sigstore/sigstore-go#647). Both sources and
# their dependency graph are pinned in tools/cosign/go.mod and go.sum.
set -euo pipefail
started=$SECONDS
destination=${1:?usage: install_cosign.sh destination}
mkdir -p "$destination"
destination=$(cd "$destination" && pwd)
repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo/tools/cosign"

# Do not inherit a workspace, flags or checksum bypass from the caller.
export GOWORK=off GOENV=off GOFLAGS=-mod=readonly GOTOOLCHAIN=local CGO_ENABLED=0
export GOSUMDB=sum.golang.org GONOSUMDB=none GOPRIVATE=none
export GOPROXY=https://proxy.golang.org
expected_go=$(awk '/^go / {print "go" $2}' go.mod)
if [[ $(go env GOVERSION) != "$expected_go" ]]; then
  echo "Cosign build requires $expected_go" >&2
  exit 1
fi
go mod download
go mod verify
go test -count=1 ./...
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT
go build -trimpath -buildvcs=false -o "$build/cosign" github.com/sigstore/cosign/v3/cmd/cosign

# Verify the installed artifact uses exactly the tested signing implementation.
go version -m "$build/cosign" > "$build/modules"
for dependency in 'github.com/sigstore/cosign/v3 v3.1.3' 'github.com/sigstore/sigstore-go v1.3.0'; do
  read -r module version <<< "$dependency"
  actual=$(awk -v module="$module" '($1 == "dep" || $1 == "mod") && $2 == module {print $3}' "$build/modules")
  if [[ "$actual" != "$version" ]]; then
    echo "Cosign dependency mismatch: $module expected $version, got $actual" >&2
    exit 1
  fi
  echo "Verified Cosign source: $module $actual"
done
mv "$build/cosign" "$destination/cosign"
echo "Verified Cosign build installed in $((SECONDS - started))s"
