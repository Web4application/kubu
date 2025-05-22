#!/bin/bash

BASE_URL="https://yourdomain.com" # Replace with your deployed URL

URLS=(
  "$BASE_URL/001.html"
  "$BASE_URL/002.jpg"
  "$BASE_URL/003.html"
  "$BASE_URL/004.html"
  "$BASE_URL/005.txt"
)

echo "Starting HTTP/2 Header Checks..."

for url in "${URLS[@]}"; do
  echo "Checking $url"
  curl -I --http2 "$url" | grep -E "HTTP|content-type|alt-svc|server"
  echo "-------------------------"
done

echo "Running h2load test on $BASE_URL/001.html (100 requests, 10 concurrency)..."

if ! command -v h2load &> /dev/null; then
  echo "h2load not found! Please install nghttp2 package first."
  exit 1
fi

h2load -n 100 -c 10 "$BASE_URL/001.html"

echo "Tests completed."
