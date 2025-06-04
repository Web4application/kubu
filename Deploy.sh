#!/bin/bash
set -e

ssh -o StrictHostKeyChecking=no $REMOTE_USER@$REMOTE_HOST << EOF
  docker pull yourdockerrepo/ai-backend:${GITHUB_SHA}
  docker stop ai-backend || true
  docker rm ai-backend || true
  docker run -d --name ai-backend -p 8000:8000 yourdockerrepo/ai-backend:${GITHUB_SHA}
EOF
