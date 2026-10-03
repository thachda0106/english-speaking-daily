#!/usr/bin/env bash
# Generate the audio for every day listed in scripts/days.py.
#
#   bash scripts/build_all_audio.sh            # all days
#   bash scripts/build_all_audio.sh 11 12 13   # only those day numbers
#
# The day -> speaker list lives in scripts/days.py, so this does not need editing
# when a new day is added. Exits 1 if any day failed.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

PY="${HERMES_PY:-/c/Users/thach/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe}"
failed=()

# Emit "<day-folder> <speaker>" per line, from the single source of truth.
plan () {
  "$PY" - <<'EOF'
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path("scripts").resolve()))
import importlib.util
spec = importlib.util.spec_from_file_location("days", "scripts/days.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
for day, speaker in sorted(mod.DAYS.items()):
    if not pathlib.Path(day, "audio").is_dir():
        continue
    print(day, speaker)
EOF
}

run_day () {
  local day="$1" prefix="$2"
  echo ""
  echo "=== $day  (prefix: $prefix) ==="
  "$PY" scripts/make_audio.py "$day" --prefix "$prefix" || {
    echo "!!! FAILED: $day"
    failed+=("$day")
    return 1
  }
}

while read -r day prefix; do
  [ -z "$day" ] && continue
  if [ $# -gt 0 ]; then
    num="${day#day-}"
    num="${num%%-*}"
    want=0
    for want_day in "$@"; do
      [ "$(printf '%02d' "$want_day" 2>/dev/null)" = "$num" ] && want=1
    done
    [ "$want" = 1 ] || continue
  fi
  run_day "$day" "$prefix"
done < <(plan)

echo ""
if [ ${#failed[@]} -gt 0 ]; then
  echo "=== FINISHED WITH ERRORS: ${failed[*]} ==="
  exit 1
fi
echo "=== all done ==="