#!/bin/bash
# Serial clean fleet over the contaminated roster, canonical guard-gated harness.
cd /Users/stevens/pi-problems-30 || exit 1
LOG=/Users/stevens/pi-problems-30/fleet_clean_queue.log
: > "$LOG"
echo "== FLEET START $(date) ==" >> "$LOG"
# provider|model|tag  (spark-direct = free Spark ollama; serial one-at-a-time)
QUEUE=(
  "spark-direct|gpt-oss:20b|clean-p1-10-gptoss20b"
  "spark-direct|qwen3-coder:30b|clean-p1-10-qwen3coder30b"
  "spark-direct|mistral-small:24b|clean-p1-10-mistralsmall24b"
  # "spark-direct|deepseek-r1:32b|clean-p1-10-deepseekr1-32b"   # REMOVED from test list (Rick, 2026-07-05)
)
for entry in "${QUEUE[@]}"; do
  IFS="|" read -r prov model tag <<< "$entry"
  echo "-- $(date) START $tag ($model) --" >> "$LOG"
  bash run_model.sh "$prov" "$model" "$tag" >> "$LOG" 2>&1
  score=$(grep -cE "P[0-9]+: PASS" "runs/$tag/RESULTS.txt" 2>/dev/null)
  echo "-- $(date) DONE $tag score=${score:-?}/10 --" >> "$LOG"
done
echo "== FLEET COMPLETE $(date) ==" >> "$LOG"
