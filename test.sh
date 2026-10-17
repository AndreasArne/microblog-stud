#!/bin/sh

set -eu

. .venv/bin/activate

mkdir -p /tmp/.pylint.d
export PYLINTHOME=/tmp/.pylint.d

exec make test
