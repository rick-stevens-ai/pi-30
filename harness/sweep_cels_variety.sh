#!/bin/bash
# Full-10 pi agent-loop sweep across a VARIETY of CELS/ALCF tool-use-capable models.
# Each model runs the complete 10-problem harness (run_model.sh). Verdicts come from
# verifier exit codes, never model prose. Sequential to avoid LiteLLM proxy contention.
set -u
export PATH="/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
cd /Users/stevens/pi-problems-30
LOG=/tmp/sweep_cels_variety.log
: > "$LOG"

# provider model-id tag  -- Qwen3-Coder is the safe tool-use pick; kimi confirmed;
# minimax + llama70 broaden the family; gpt-oss is the wrap-and-retry case.
RUNS=(
  "litellm-cherryrd alcf/Qwen3-Coder-480B qwen3coder480b"
  "litellm-cherryrd alcf/Kimi-K2.5 kimi25"
  "litellm-cherryrd alcf/MiniMax-M2.5 minimax25"
  "litellm-cherryrd cels/llama70 llama70"
  "litellm-cherryrd alcf/gpt-oss-120b gptoss120alcf"
)

echo "==== CELS-VARIETY SWEEP START $(date) ====" | tee -a "$LOG"
for r in "${RUNS[@]}"; do
  set -- $r
  PROV="$1"; MODEL="$2"; TAG="$3"
  echo "---- $(date) launching $TAG ($MODEL) ----" | tee -a "$LOG"
  bash run_model.sh "$PROV" "$MODEL" "$TAG" >>"$LOG" 2>&1
  echo "---- $(date) finished $TAG ----" | tee -a "$LOG"
  echo "SUMMARY $TAG:" | tee -a "$LOG"
  grep -E "P[0-9]+: (PASS|FAIL|STOP)" "runs/$TAG/RESULTS.txt" 2>/dev/null | tee -a "$LOG"
done
echo "==== CELS-VARIETY SWEEP DONE $(date) ====" | tee -a "$LOG"
