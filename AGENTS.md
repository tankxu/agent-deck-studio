# Working in this repository (for coding agents)

Read docs/METHOD.md first: it describes the workflow this repo is built for.

- Source of slides: `deck/deck.py`. Rebuild with `python3 tools/build.py` after every change.
- Every visible string must go through `E(key, default)` (or `T`) so it stays editable and lands in `deck-content.json`. Keys are stable ids, not page numbers.
- `deck-content.json` is shared with people editing in the browser. Never delete or rewrite its `texts` to “refresh” defaults; the build updates a value only when it still equals its previous default (`defaults`), so human edits survive.
- Link to slides with `data-chapter="<slide id>"`; the build turns it into page numbers.
- After changing slides: `tools/qa-shots.sh && tools/qa-sheet.sh`, then look at `.qa/sheet-*.png` for overflow, empty space, missing images, wrong branding, consecutive text-only pages.
- Record each round in `deck/versions.py`: what changed and every question raised (who, question, resolution) — including the ones not adopted and why.
- Source material lives in `sources/` (git-ignored). Write only from it; do not invent figures. Put the provenance of each number in the slide's `notes`.
- Mark drawn interface mockups as 示意 and keep stat-like numbers out of them.
- Concept art: write the prompt in `concept(key, label, prompt)`; prompts are collected in `deck-content.json` → `conceptPrompts`; generated images go to `assets/concept/<key>.jpg`.
