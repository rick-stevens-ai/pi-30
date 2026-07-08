#!/bin/bash
# Sophia/ALCF full-10 pi agent-loop sweep — Ollie's half of the full-10 cross-model matrix.
# Models: the ALCF Sophia models NOT already covered by Kukla's m1 sweep
# (Kukla owns: Qwen3-Coder-480B, Kimi-K2.5, MiniMax-M2.5, llama70, gpt-oss-120b via ALCF)
# We run: Llama-3.1-8B, Llama-3.1-70B, Llama-3.3-70B, Llama-4-Scout, Llama-4-Maverick,
#         gemma-3-27b, Mixtral-8x22B, gpt-oss-20b — all via litellm-cherryrd alcf/...
# Each gets the full run_model.sh (tool-use harness, verdicts from verifier exit codes only).
# Sequential to avoid LiteLLM proxy contention.

set -u
export PATH="/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
cd /Users/stevens/pi-problems-30
LOG=/tmp/sweep_sophia.log
: > "$LOG"

# provider model-id tag — tag used as runs/<tag>/RESULTS.txt path
RUNS=(
  "litellm-cherryrd alcf/Meta-Llama-3.1-8B-Instruct sophia-llama31-8b"
  "litellm-cherryrd alcf/Meta-Llama-3.1-70B-Instruct sophia-llama31-70b"
  "litellm-cherryrd alcf/Llama-3.3-70B-Instruct sophia-llama33-70b"
  "litellm-cherryrd alcf/Llama-4-Scout-17B-16E-Instruct sophia-llama4-scout"
  "litellm-cherryrd alcf/Llama-4-Maverick-17B-128E-Instruct sophia-llama4-maverick"
  "litellm-cherryrd alcf/gpt-oss-20b sophia-gptoss20b"
  "litellm-cherryrd alcf/google/gemma-3-27b-it sophia-gemma3-27b"
  "litellm-cherryrd alcf/mistralai/Mixtral-8x22B-Instruct-v0.1 sophia-mixtral-8x22b"
)

echo "==== SOPHIA SWEEP START $(date) ====" | tee -a "$LOG"
for r in "${RUNS[@]}"; do
  set -- $r
  PROV="$1"; MODEL="$2"; TAG="$3"
  echo "---- $(date) launching $TAG ($MODEL) ----" | tee -a "$LOG"
  bash run_model.sh "$PROV" "$MODEL" "$TAG" >>"$LOG" 2>&1
  echo "---- $(date) finished $TAG ----" | tee -a "$LOG"
  echo "SUMMARY $TAG:" | tee -a "$LOG"
  grep -E "P[0-9]+: (PASS|FAIL|STOP)" "runs/$TAG/RESULTS.txt" 2>/dev/null | tee -a "$LOG"
  echo "---" | tee -a "$LOG"
done

echo "==== SOPHIA SWEEP DONE $(date) ====" | tee -a "$LOG"
echo ""
echo "===== FINAL SUMMARY =====" | tee -a "$LOG"
for r in "${RUNS[@]}"; do
  set -- $r
  TAG="$3"
  PASSES=$(grep -c "P[0-9]*: PASS" "runs/$TAG/RESULTS.txt" 2>/dev/null || echo 0)
  FAILS=$(grep -c "P[0-9]*: FAIL" "runs/$TAG/RESULTS.txt" 2>/dev/null || echo 0)
  printf "%-32s PASS=%s FAIL=%s\n" "$TAG" "$PASSES" "$FAILS" | tee -a "$LOG"
done
