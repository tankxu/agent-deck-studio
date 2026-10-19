#!/bin/sh
# Export the deck to PDF from the command line with the same in-page renderer as the
# “导出 PDF” button (headless Chrome over CDP). Needs a server on DECK_URL (default :8793).
# Usage: tools/export-pdf.sh [output.pdf]
OUT="${1:-deck.pdf}"
node "$(dirname "$0")/qa-pdf.mjs" "$OUT" "" "${DECK_URL:-http://127.0.0.1:8793/}"
