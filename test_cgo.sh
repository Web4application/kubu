#!/bin/bash
set -euo pipefail

echo "Checking CGO availability..."

# Detect if CC is set
if [ -z "${CC-}" ]; then
  echo "No CC variable set, trying default compiler detection..."

  # Temporarily clear PATH except Go bin directory to test compiler presence
  OLD_PATH="$PATH"
  export PATH="$GOROOT/bin"

  # Check if compiler is found via 'go env'
  CGO_DEFAULT=$(go env CGO_ENABLED)

  if [ "$CGO_DEFAULT" == "1" ]; then
    echo "Compiler detected in default path. CGO_ENABLED=1"
    export CGO_ENABLED=1
  else
    echo "No compiler detected. CGO_ENABLED=0"
    export CGO_ENABLED=0
  fi

  export PATH="$OLD_PATH"
else
  echo "CC is set to '$CC', forcing CGO_ENABLED=1"
  export CGO_ENABLED=1
fi

echo "Final CGO_ENABLED=$CGO_ENABLED"
