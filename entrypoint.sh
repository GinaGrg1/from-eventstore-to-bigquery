#!/bin/sh

# exit on error
set -e

# print command
set -o xtrace

# colours
export TERM=xterm-256color

unset `env | grep affinity | awk -F= '/^\w/ {print $1}' | xargs`
DATE=`/bin/date +%Y-%m-%d-%H:%M:%S`

cd /code/src

if [ "$1" == "data-river-run-jenkins" ]; then
    python -m unittest discover tests
    exit $?
fi

if [ "$1" == "data-river-run-test" ]; then
    python main.py
fi

if [ "$1" == "data-river-run-prod" ]; then
    python main.py
fi