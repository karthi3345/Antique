#!/bin/sh
# Vercel build: migrate + seed when a database is reachable, then collectstatic.
# Keeps the deployment green even if DATABASE_URL is unset or the DB is down;
# runtime DB failures surface as Django errors, not broken builds.
set -e

if [ -n "$DATABASE_URL" ]; then
  echo "DATABASE_URL set -- applying migrations"
  python3 manage.py migrate --noinput
  echo "Seeding collection (idempotent)"
  python3 manage.py seed_volgo
else
  echo "No DATABASE_URL -- skipping database steps"
fi

python3 manage.py collectstatic --noinput
