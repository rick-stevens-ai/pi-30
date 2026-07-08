#!/bin/bash
# Aggregator B full sweep — runs the 10-problem traced loop across all B models
# sequentially, appends a bucket CSV row per model, pings Ollie as rows land.
# Skips models already done (resume-safe). Self-contained; run via terminal background tool.
set -u
export PATH="/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
SRC=/Users/stevens/pi-problems-30
cd "$SRC"
source ~/Dropbox/AIEN/env.sh 2>/dev/null
CSV=/Users/stevens/Dropbox/XFER/multimodel-sweep/aggregator-b/aggB_buckets_20260629.csv
[ -f "$CSV" ] || echo "label,provider,model,fleet,bucket,latency_s,evidence" > "$CSV"

# Model order: LM Studio FIRST (m3acbook, fast + uncontended), Spark LAST
# (Spark/Ollama observed very slow even at low util 2026-06-30; don't let it block
#  the fast LMStudio lane). Resume-safe: completed P10 runs are skipped.
MODELS=(
  lmstudio/gpt-oss-120b lmstudio/gpt-oss-20b lmstudio/qwen3-coder-30b
  lmstudio/qwen3-next-80b lmstudio/seed-oss-36b lmstudio/glm-4.7-flash
  lmstudio/gemma-3-27b
  lmstudio/llama-3.3-70b lmstudio/qwq-32b
  spark/codestral-22b spark/devstral-small-2-24b
  spark/mistral-small-24b spark/qwen3-14b
  spark/gpt-oss-120b spark/gpt-oss-20b spark/qwen3-coder-30b spark/glm-4.7-flash
 
)

tag_of() { echo "aggB-$(echo "$1" | tr '/' '-')"; }

for m in "${MODELS[@]}"; do
  tag=$(tag_of "$m")
  # resume guard: skip if a complete RESULTS.txt (has P10:) already exists
  if [ -f "runs/$tag/RESULTS.txt" ] && grep -q "^P10:" "runs/$tag/RESULTS.txt"; then
    echo "[skip] $tag already complete"
    continue
  fi
  echo "[run ] $tag  ($(date -u +%H:%M:%S))"
  t0=$(date +%s)
  # per-model wall cap: 45min. A model that can't finish 10 problems in 45min
  # (Spark slowness) is bucketed from whatever completed, not allowed to eat hours.
  timeout 2700 bash run_model_traced.sh aggregator-b "$m" "$tag" >/dev/null 2>&1
  t1=$(date +%s); dur=$((t1-t0))
  R="runs/$tag/RESULTS.txt"
  # count clean per-problem passes (avoid double-count of 'round' lines)
  pass=0
  for i in $(seq 1 10); do grep -qE "^P$i: PASS" "$R" 2>/dev/null && pass=$((pass+1)); done
  if [ "$pass" -ge 10 ]; then bucket=pass
  elif [ "$pass" -ge 4 ]; then bucket=plateau
  else bucket=fail; fi
  ev=$(for i in $(seq 1 10); do grep -qE "^P$i: PASS" "$R" && printf "P%s+" "$i"; done | sed 's/+$//')
  echo "aggB-$(echo "$m"|tr '/' '-'),aggregator-b,$m,aggB,$bucket,$dur,\"$pass/10 $ev\"" >> "$CSV"
  # ping Ollie per model
  kukla-mail send "[Kukla aggB] $m -> $pass/10 ($bucket), ${dur}s. Row appended to XFER/multimodel-sweep/aggregator-b/." >/dev/null 2>&1
done

echo "==== AGGREGATOR B SWEEP COMPLETE $(date) ===="
echo "CSV: $CSV"
cat "$CSV"
