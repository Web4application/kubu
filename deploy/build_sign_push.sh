#!/bin/bash
set -e

IMAGE_NAME="ghcr.io/web4application/kubuverse:latest"

echo "Creating and using Docker Buildx builder..."
docker buildx create --use --name kubu-builder || docker buildx use kubu-builder

echo "Building and pushing multi-arch image..."
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t $IMAGE_NAME \
  --push .

echo "Signing the image with Cosign..."
if [ -z "$COSIGN_PASSWORD" ]; then
  echo "COSIGN_PASSWORD environment variable not set! Aborting..."
  exit 1
fi

cosign sign --key cosign.key $IMAGE_NAME

echo "Verifying the image signature..."
cosign verify --key cosign.pub $IMAGE_NAME

echo "Done! Image built, pushed, and signed successfully."
