"""Canonical runs.csv schema for the pi-30 course adapters (Lab 1, CMSC 35200).

One row per ATTEMPT (an agent's single turn on a task). The verifier/scorer EXIT
CODE is the sole source of truth for status — never the agent's prose.

Use the literal string "unknown" (not 0, not blank) when a runtime does not
expose a field (e.g. a CLI that does not report token counts).
"""
from __future__ import annotations
import csv, os, io

FIELDS = [
    "agent",             # "pi" | "codex"
    "task_id",           # P1..P30
    "attempt",           # 1-based attempt index within this task
    "start_utc",         # ISO-8601 UTC
    "end_utc",           # ISO-8601 UTC
    "wall_seconds",      # float, whole-attempt wall clock
    "status",            # infra_error | invalid_output | task_failed | verified_success | not_run
    "verifier_status",   # pass | fail | error | not_run   (from verifier exit code)
    "score",             # numeric score where applicable (optimize/tournament); else "unknown"
    "prompt_tokens",
    "completion_tokens",
    "reasoning_tokens",
    "total_tokens",
    "tool_calls",
    "retry_count",       # retries the AGENT made inside this attempt (if known) else "unknown"
    "model",
    "endpoint_label",
    "pi_or_codex_version",
    "harness_commit",
    "stdout_path",
    "stderr_path",
    "transcript_path",
]

UNKNOWN = "unknown"


def new_row(**kw):
    row = {f: UNKNOWN for f in FIELDS}
    row.update({k: v for k, v in kw.items() if k in FIELDS})
    return row


def write_header_if_needed(path):
    exists = os.path.exists(path) and os.path.getsize(path) > 0
    if not exists:
        with open(path, "a", newline="") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def append_row(path, row):
    write_header_if_needed(path)
    full = new_row(**row)
    with open(path, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow(full)
    return full
