#!/bin/bash

mkdir -p certs

openssl req -x509 -newkey rsa:4096 -sha256 -days 365 \
  -nodes -keyout certs/server.key -out certs/server.crt \
  -subj "/CN=localhost" \
  -addext "subjectAltName = DNS:localhost"

echo "✅ Self-signed certificate generated in ./certs/"
