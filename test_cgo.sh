#!/bin/bash

echo "Assume we're on a system that can enable cgo normally."
export CGO_ENABLED=
go env CGO_ENABLED
echo "Expected output: 1"

echo "Clearing CC and removing everything but Go from the PATH should usually disable cgo."
export CC=
export PATH=$GOROOT/bin
go env CGO_ENABLED
echo "Expected output: 0 (if no absolute default CC path exists) or 1 (if default CC path exists)"

echo "Setting CC should re-enable cgo."
export CC=cc
go env CGO_ENABLED
echo "Expected output: 1"

echo "Setting CGO_ENABLED should enable cgo."
export CC=
export CGO_ENABLED=1
go env CGO_ENABLED
echo "Expected output: 1"
