#!/bin/bash
# Volgo - run all test suites (django + node). Exit non-zero on any failure.
set -e
cd "$(dirname "$0")/.."

echo "== Django tests =="
python3 manage.py test --no-input -v 1 --settings=config.test_settings

echo "== Node tests (post animation) =="
node static/tests/post.test.js

echo "ALL TESTS PASSED"
