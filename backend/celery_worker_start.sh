#!/bin/bash
celery -A app.worker.celery_app worker --loglevel=info
