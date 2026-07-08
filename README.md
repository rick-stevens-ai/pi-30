# pi-30 — Agent-Loop Fleet Benchmark

A 30-problem agentic coding benchmark for the [pi agent CLI](https://github.com/) (Earendil Pi).
Each problem is graded by a **machine-checkable verifier** whose **exit code** is the sole
source of truth — the model's prose is never trusted for scoring. Problems exercise five skill
families: **write** (build a utility from a spec), **fix** (repair a seeded-broken module),
**numerical** (implement to a tolerance), **optimize** (beat a performance baseline), and
**tournament** (self-critique / converge).

This repo is the canonical home for the problem set, the run harness, every model lane's
evidence, and the published report + slide deck.

## Layout

```
problems/         p1 .. p30 — each dir holds the verifier (verify.py / check.py / bench.py /
                  score.py / test_thing.py / converge_check.py) plus seed scaffolding files.
                  The PROBLEM STATEMENTS themselves are embedded in harness/run_model_30.sh
                  (one prompt block per problem).
harness/          run_model_30.sh   — the 30-problem runner (the source of truth for prompts)
                  run_model_10.sh   — legacy P1-P10 runner
                  driver.sh         — original 10-problem driver
                  fleet_*.sh        — parallel fleet launch / resume / report helpers
                  sweep_*.sh        — provider-specific sweep launchers (CELS, OpenRouter, Sophia, sparks)
                  or_backoff_proxy.py — OpenRouter 429 backoff proxy (reads key from ~/.pi/agent/models.json)
                  extract_code.py, setsid_shim.py — utilities
                  litellm_m1_config.yaml — local LiteLLM model map (placeholder keys only)
                  ENGINEERING_NOTES.md — harness design notes & pitfalls
runs/             one dir per model lane (e.g. fleet-gemma4-12b-*/), each with pN/ artifacts
                  + RESULTS.txt. _logs/ holds per-run stdout logs.
final_results/    frozen RESULTS.txt snapshots for the CELS-served lanes.
report/           FLEET_BENCHMARK_REPORT.tex/.pdf + FLEET_BENCHMARK_TABLES.tex
deck/             gen_pi30.cjs (pptxgenjs generator) + deck_lib.cjs + pi30_Fleet_Benchmark.pptx
FLEET_BENCHMARK_MASTER.md   — the integrated 24-lane master table + per-problem analysis
```

## Running a lane

```bash
cd harness
PI_TIMEOUT=360 bash run_model_30.sh <provider> <model-id> <tag> > runs30_<tag>.log 2>&1
# e.g.
PI_TIMEOUT=360 bash run_model_30.sh laguna-uicgpu laguna-xs2 laguna-xs2 > runs30_laguna-xs2.log 2>&1
```

Results land in `runs30/<tag>/` (RESULTS.txt + per-problem artifacts). Verdicts come from
verifier **exit codes**, never pi prose.

## Scoring rules (standing)

- **Single-shot is canonical.** A targeted rerun of only the missed problems is *not* promoted
  to the headline score; the fair way to claim a true 30/30 is a k-of-N full sweep, same method
  for every model.
- **Zero-score rule.** Any `0/N` is treated as a **server/harness/stack failure**, debugged as
  infrastructure, and marked `BROKEN-<cause>` — never published as a capability result.
- **Three segmented sets, never cross-merged:** Fleet-30 (P1–P30, this repo), aggB-10 (P1–P10),
  and mesh-extract-10 (10-problem subset). This repo is the Fleet-30 set.

## Platform naming (report/deck convention)

Backends are labeled by hardware/vendor, not host codename: **Intel PVC** (Data Center GPU Max
1550), **nVIDIA A100** (8×A100-80GB DGX), **local dgx** (locally-served DGX endpoints),
**spark (ollama)**, **OpenRouter**.

## Environment pitfalls baked into the harness

- `unset PYTHONPATH` + `export CONDA_NO_PLUGINS=true` at the top of `run_model_30.sh` — a leaked
  user-site `py.py` shadows the real `py` package and false-fails every pytest problem.
- Every pi call is wrapped in `gtimeout` (a hung endpoint would otherwise wedge a sequential
  lane for hours); every `score.py` call is wrapped too (pathological candidate kernels).

See `harness/ENGINEERING_NOTES.md` for the full list.
