#!/bin/bash
# pi P1-P30 sweep — OLLIE's lane: 3 sparks + Argo, extend the cross-model matrix to 30.
# Each spark runs its model list SERIALLY (ollama JIT-swaps one resident model at a time);
# the 3 spark chains + the Argo chain run in PARALLEL across boxes.
# Canonical harness run_model_30.sh, canonical ~/pi-problems-30 seed set, guard on.
export PATH="/Users/stevens/bin:/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
cd /Users/stevens/pi-problems-30 || exit 1
mkdir -p final_results runs30_logs
STAMP=$(date +%Y%m%d-%H%M%S)

run1() {  # provider model tag
  local prov="$1" model="$2" tag="$3"
  echo "[start $(date +%H:%M:%S)] $tag ($prov / $model)"
  bash run_model_30.sh "$prov" "$model" "$tag" > "runs30_logs/${tag}.log" 2>&1
  cp "runs/$tag/RESULTS.txt" "final_results/${tag}.RESULTS.${STAMP}.txt" 2>/dev/null
  echo "[done  $(date +%H:%M:%S)] $tag"
}

chain() { for t in "$@"; do :; done; }  # placeholder

# spark-36ac chain
( run1 spark36 qwen3-coder:30b      spark36-qwen3coder30b
  run1 spark36 gpt-oss:120b         spark36-gptoss120b
  run1 spark36 devstral-small-2:24b spark36-devstral2-24b
) > runs30_logs/CHAIN-spark36.log 2>&1 &
echo "spark36 chain PID $!"

# spark-95fe chain
( run1 spark-95fe gpt-oss:20b           spark95-gptoss20b
  run1 spark-95fe glm-4.7-flash:latest  spark95-glm47flash
  run1 spark-95fe nemotron-3-super:120b spark95-nemotron3super120b
) > runs30_logs/CHAIN-spark95.log 2>&1 &
echo "spark95 chain PID $!"

# spark-9611 chain
( run1 spark-9611 codestral:22b       spark9611-codestral22b
  run1 spark-9611 mistral-small:24b   spark9611-mistralsmall24b
  # run1 spark-9611 deepseek-r1:32b     spark9611-deepseekr1-32b   # REMOVED from test list (Rick, 2026-07-05)
  run1 spark-9611 qwen3:14b           spark9611-qwen3-14b
) > runs30_logs/CHAIN-spark9611.log 2>&1 &
echo "spark9611 chain PID $!"

# Argo chain
( run1 argo argo:claude-opus-4.7   argo-opus47
  run1 argo argo:claude-sonnet-4.6 argo-sonnet46
) > runs30_logs/CHAIN-argo.log 2>&1 &
echo "argo chain PID $!"

echo "=== 4 chains launched at $STAMP ==="
wait
echo "=== ALL DONE $(date) ==="
