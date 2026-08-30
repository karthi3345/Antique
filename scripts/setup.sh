#!/bin/bash
# Volgo — setup on every deploy / container start.
set -e
cd /workspace

# 1. Install dependencies
pip install --quiet --break-system-packages -r requirements.txt

# 2. Apply migrations (idempotent)
python3 manage.py migrate --noinput

# 3. Seed the collection from the museum archive (idempotent)
python3 manage.py seed_volgo

# 4. Collect static files for production serving
python3 manage.py collectstatic --noinput --clear

echo "Volgo setup complete."
