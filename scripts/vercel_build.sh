#!/bin/sh
# Vercel build: try DB setup (migrate + seed) when a database is reachable,
# then collectstatic. DB steps are best-effort: the WSGI cold-start
# bootstrap retries them at runtime, so a sandboxed/unreachable DB at
# build time must never fail the deployment.
set -e

if [ -n "$DATABASE_URL" ]; then
  echo "DATABASE_URL set -- attempting migrations + seed"
  python3 manage.py migrate --noinput || echo "WARN: migrate failed at build time; will retry at runtime"
  python3 manage.py seed_volgo || echo "WARN: seed failed at build time; will retry at runtime"
else
  echo "No DATABASE_URL -- skipping database steps"
fi

python3 manage.py collectstatic --noinput
