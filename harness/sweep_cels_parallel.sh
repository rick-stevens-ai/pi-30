#!/bin/bash
# Kukla's parallel CELS-fleet P1-P10 clean sweep.
# 4 CELS models on different backends -> run SIMULTANEOUSLY, each its own
# fresh run dir + log. run_model.sh self-guards on contamination + stages a
# clean dir per tag. Verdicts from verifier exit codes.
set -u
cd /Users/stevens/pi-problems-30
TS=$(date +%Y%m%dT%H%M%SZ)
LOGDIR=/Users/stevens/pi-problems-30/runs/_parallel_$TS
mkdir -p "$LOGDIR"

launch() {  # launch <provider> <model> <tag>
  echo ">>>> $(date) starting $3" | tee -a "$LOGDIR/$3.log"
  bash run_model.sh "$1" "$2" "$3" >> "$LOGDIR/$3.log" 2>&1
  echo ">>>> $(date) finished $3 (exit $?)" | tee -a "$LOGDIR/$3.log"
}

launch litellm-cherryrd cels/oss120     oss120   &
launch litellm-cherryrd cels/llama70    llama70  &
launch cels-chicago-4   nemotron-3-ultra nemotron &
launch litellm-cherryrd cels/kimi-k2.6  kimi     &
wait

echo "==== PARALLEL CELS P1-P10 SWEEP COMPLETE $(date) ===="
echo "=== combined scorecard ==="
for t in kimi oss120 llama70 nemotron; do
  f=/Users/stevens/pi-problems-30/runs/$t/RESULTS.txt
  echo "----- $t -----"
  grep -E "P[0-9]+: (PASS|FAIL|STOP)" "$f" 2>/dev/null
  p=$(grep -cE "P[0-9]+: PASS" "$f" 2>/dev/null); echo "  $t PASS count: ${p:-0}/10"
done
echo "logs: $LOGDIR"
