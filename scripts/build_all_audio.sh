#!/usr/bin/env bash
# Generate all remaining day audio, one day at a time.
set -u
cd "$(dirname "$0")/.." || exit 2

PY="${HERMES_PY:-/c/Users/thach/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe}"

run_day () {
  local day="$1" prefix="$2"
  echo ""
  echo "=== $day  (prefix: $prefix) ==="
  "$PY" scripts/make_audio.py "$day" --prefix "$prefix" || {
    echo "!!! FAILED: $day"
    return 1
  }
}

run_day day-07-salary-discussion      recruiter
run_day day-08-negotiating-a-deadline manager
run_day day-09-small-talk-at-lunch   colleague
run_day day-10-technical-interview   interviewer

echo ""
echo "=== all done ==="
