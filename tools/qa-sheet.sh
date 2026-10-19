#!/bin/sh
# Contact sheets (12 slides each) from qa-shots output. Usage: tools/qa-sheet.sh [dir]
D="$(cd "${1:-.qa/v4}" && pwd)"; cd "$D"; set -- $(ls [0-9]*.png); total=$#; s=0
while [ $s -lt $total ]; do
  f="$D/sheet-$s.html"; echo "<html><body style='margin:0;background:#555;display:grid;grid-template-columns:repeat(3,800px);gap:6px;padding:6px;width:2418px'>" > "$f"
  i=0; for p in "$@"; do if [ $i -ge $s ] && [ $i -lt $((s+12)) ]; then echo "<div style='position:relative'><img src='$p' style='width:800px;display:block'><b style='position:absolute;left:6px;top:6px;background:#f00;color:#fff;font:bold 18px sans-serif;padding:2px 6px'>$((i+1))</b></div>" >> "$f"; fi; i=$((i+1)); done
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --allow-file-access-from-files --window-size=2418,1830 --screenshot="$D/sheet-$s.png" "file://$f" 2>/dev/null
  s=$((s+12))
done; ls "$D"/sheet-*.png
