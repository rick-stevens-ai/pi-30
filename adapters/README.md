# pi-30 Course Adapters (CMSC 35200 — Lab 1)

Official **Pi** and **Codex** adapters that run the 30 problems and emit a single
canonical `runs.csv` (one row per attempt). The verifier/scorer **exit code** is the
sole source of truth — agent prose is never scored.

## Files
- `runs_schema.py` — the canonical 22-column `runs.csv` schema (agent + the 21 required fields).
- `common.py` — shared runner: fresh-workspace staging per task, iterate-until-green loop
  (feeds verifier failure output back on retries), artifact flatten, verifier exit-code
  authority, per-attempt row emission.
- `tasks_spec.json` — the 30 tasks (title, kind, verifier, iteration budget, prompts),
  extracted from `harness/run_model_30.sh`.
- `pi_adapter.py` — drives the Pi coding agent.
- `codex_adapter.py` — drives Codex CLI (requires `wire_api="responses"`; see Lab 1 Part A).
- `run_lab1_benchmark.sh` — orchestrator: runs the seed guard, then both agents, then prints a summary.

## Prerequisites (Lab 1 Part A)
- `pi` and `codex` installed and on PATH (npm global bin, e.g. `~/.npm-global/bin`).
- Pi provider `dls-qwen` configured in `~/.pi/agent/models.json`.
- Codex provider `dls_qwen` configured in `~/.codex/config.toml` with
  `base_url=<chicago-6>/v1`, `wire_api="responses"`, `env_key="DLS_QWEN_API_KEY"`.
- `DLS_QWEN_API_KEY` exported in the shell. **Adapters never take an API key on the CLI.**

## Run
```bash
# full 30-problem paired run (both agents)
bash adapters/run_lab1_benchmark.sh

# a slice
bash adapters/run_lab1_benchmark.sh P1,P3,P10

# single agent
python3 adapters/pi_adapter.py    --tasks P1,P2 --csv ./runs.csv
python3 adapters/codex_adapter.py --tasks P1,P2 --csv ./runs.csv
```

## runs.csv columns
`agent, task_id, attempt, start_utc, end_utc, wall_seconds, status, verifier_status,
score, prompt_tokens, completion_tokens, reasoning_tokens, total_tokens, tool_calls,
retry_count, model, endpoint_label, pi_or_codex_version, harness_commit, stdout_path,
stderr_path, transcript_path`

`status` ∈ {infra_error, invalid_output, task_failed, verified_success, not_run}.
Use the literal `unknown` when a runtime does not expose a field (the Pi `--print` CLI
does not report token counts; Codex reports a total-token figure which is captured).
