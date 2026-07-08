#!/bin/bash
# Re-run fan-out problems (P7/P17/P25) with the FIXED harness across every model
# whose original run false-failed them. Sparks run SERIALLY per-box (ollama swaps
# one resident model at a time); separate boxes + openrouter run in PARALLEL.
cd /Users/stevens/pi-problems-30
mkdir -p runs30_logs
R="bash rerun_fanout.sh"

# spark-95fe chain (serial)
( $R spark-95fe glm-4.7-flash:latest  clean-glm47flash-v2
  $R spark-95fe nemotron-3-super:120b clean-nemotron3super-v2
  $R spark-95fe nemotron-3-super:120b spark95-nemotron3super120b
  $R spark-95fe nemotron3:33b         local-nemotron3-33b
  $R spark-95fe nemotron-3-nano:30b   local-nemotron3-nano-30b
) > runs30_logs/FANOUT-spark95.log 2>&1 &
echo "spark95 chain PID $!"

# spark-9611 chain (serial) — DROPPED: deepseek-r1 removed from test list (Rick, 2026-07-05).
# qwen3:14b handled separately by smoke run. Chain now empty; left as a no-op.
# ( $R spark-9611 deepseek-r1:32b-tools clean-deepseekr1-32b-tools-v2
#   $R spark-9611 deepseek-r1:32b       spark9611-deepseekr1-32b
# ) > runs30_logs/FANOUT-spark9611.log 2>&1 &
# echo "spark9611 chain PID $!"

# openrouter chain (serial, its own rate limits)
( $R openrouter-free nvidia/nemotron-3-super-120b-a12b:free or-nemotron3super-120b
) > runs30_logs/FANOUT-openrouter.log 2>&1 &
echo "openrouter chain PID $!"

wait
echo "==== ALL FANOUT RERUN CHAINS DONE $(date) ===="
