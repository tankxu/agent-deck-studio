#!/bin/sh
# Screenshot every slide; see tools/qa-shots.mjs. Usage: tools/qa-shots.sh [outdir] [first] [last]
# Needs server.py running; DECK_URL overrides the address (default http://127.0.0.1:8793/).
exec node "$(dirname "$0")/qa-shots.mjs" "$@"
