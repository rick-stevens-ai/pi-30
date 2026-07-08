#!/bin/bash
cd /Users/stevens/pi-problems-30 || exit 1
LOG=/Users/stevens/pi-problems-30/fleet_clean_queue.log
# wait for the primary fleet to finish (its PID passed as $1)
while kill -0 "$1" 2>/dev/null; do sleep 20; done
echo "== FOLLOWON START $(date) ==" >> "$LOG"
for entry in "spark-direct|gpt-oss:120b|clean-p1-10-gptoss120b" "spark-direct|devstral-small-2:24b|clean-p1-10-devstral2-24b"; do
  IFS="|" read -r prov model tag <<< "$entry"
  echo "-- $(date) START $tag --" >> "$LOG"
  bash run_model.sh "$prov" "$model" "$tag" >> "$LOG" 2>&1
  score=$(grep -cE "P[0-9]+: PASS" "runs/$tag/RESULTS.txt" 2>/dev/null)
  echo "-- $(date) DONE $tag score=${score:-?}/10 --" >> "$LOG"
done
echo "== FOLLOWON COMPLETE $(date) ==" >> "$LOG"
