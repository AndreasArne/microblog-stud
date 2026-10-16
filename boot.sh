#!/bin/sh
set -eu

while ! .venv/bin/flask db upgrade; do
    echo "Database upgrade failed, retrying in 5 seconds" >&2
    sleep 5
done
exec .venv/bin/gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
