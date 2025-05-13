#!/bin/bash
set -a
source .env
set +a

if [ -n "$1" ]; then
    # IF a file is provided as argument, execute it
    psql -f "$1"
else
    # Otherwise, connect to psql
    psql
fi