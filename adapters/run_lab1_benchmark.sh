#!/bin/bash
# Lab 1 pi-30 paired benchmark orchestrator (CMSC 35200).
# Runs BOTH agents (Pi and Codex) across the 30 problems under identical controls
# and appends every attempt to one runs.csv. Verifier exit code is the authority.
#
# Prereqs (Part A): pi + codex installed; Pi provider "dls-qwen" and Codex provider
# "dls_qwen" (wire_api="responses") configured; DLS_QWEN_API_KEY exported.
#
# Usage:
#   bash adapters/run_lab1_benchmark.sh [TASKS]
#     TASKS: optional comma list e.g. P1,P2,P3 (default: all 30)
# Env overrides: PI30_PY, PI_BIN, CODEX_BIN, MODEL, ENDPOINT_LABEL, CSV, RUNS, PI_TIMEOUT, CODEX_TIMEOUT
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(dirname "$HERE")"
TASKS="${1:-}"
MODEL="${MODEL:-qwen3.8-27b}"
ENDPOINT_LABEL="${ENDPOINT_LABEL:-chicago-6}"
PROBLEMS="${PROBLEMS:-$REPO/problems}"
RUNS="${RUNS:-$REPO/runs_lab1}"
CSV="${CSV:-$REPO/runs.csv}"
PY="${PI30_PY:-python3}"

# Seed guard MUST pass first (proves scaffolds are broken; no contamination).
echo "== Seed guard =="
if ! bash "$REPO/harness/assert_seeds_fail.sh" >/dev/null 2>&1; then
  echo "WARNING: assert_seeds_fail.sh did not return 0 — inspect before trusting results." >&2
fi

echo "== Pi lane =="
"$PY" "$HERE/pi_adapter.py" --model "$MODEL" --endpoint-label "$ENDPOINT_LABEL" \
  --problems "$PROBLEMS" --runs "$RUNS" --csv "$CSV" \
  ${TASKS:+--tasks "$TASKS"} ${PI_BIN:+--pi "$PI_BIN"} ${PI_TIMEOUT:+--timeout "$PI_TIMEOUT"}

echo "== Codex lane =="
"$PY" "$HERE/codex_adapter.py" --model "$MODEL" --endpoint-label "$ENDPOINT_LABEL" \
  --problems "$PROBLEMS" --runs "$RUNS" --csv "$CSV" \
  ${TASKS:+--tasks "$TASKS"} ${CODEX_BIN:+--codex "$CODEX_BIN"} ${CODEX_TIMEOUT:+--timeout "$CODEX_TIMEOUT"}

echo "== Done. runs.csv -> $CSV =="
"$PY" - "$CSV" <<'PY'
import csv,sys
rows=list(csv.DictReader(open(sys.argv[1])))
from collections import Counter
print("attempts:",len(rows))
by=Counter((r["agent"],r["status"]) for r in rows)
for k,v in sorted(by.items()): print(" ",k,v)
PY
