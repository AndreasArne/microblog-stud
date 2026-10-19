#!/bin/sh
set -e

until flask db upgrade; do
    echo "Upgrade command failed, retrying in 5 secs..."
    sleep 5
done

exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - microblog:app
