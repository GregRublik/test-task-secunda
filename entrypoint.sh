#!/bin/sh
set -e

echo "Running migrations..."
alembic upgrade head

echo "Seeding database..."
python -m db.seed

echo "Starting FastAPI..."
uvicorn src.main:app --host 0.0.0.0 --port ${APP_PORT}
