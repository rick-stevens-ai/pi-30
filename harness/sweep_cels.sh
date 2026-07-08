#!/bin/bash
# Kukla's CELS-fleet sweep: run the 10-problem harness against each CELS model
# sequentially. kimi-k2.6 is handled by the original driver.sh run already in
# flight; this covers the rest of the CELS fleet.
set -u
cd /Users/stevens/pi-problems-30

# provider  model-id            tag
run() { echo ">>>> $(date) starting $3"; bash run_model.sh "$1" "$2" "$3"; echo ">>>> $(date) finished $3"; }

run litellm-cherryrd cels/oss120          oss120
run litellm-cherryrd cels/llama70         llama70
run cels-chicago-4   nemotron-3-ultra     nemotron
run litellm-cherryrd cels/kimi-k2.6       kimi

echo "==== CELS FLEET SWEEP COMPLETE $(date) ===="
echo "=== combined summaries ==="
for t in kimi oss120 llama70 nemotron; do
  f=/Users/stevens/pi-problems-30/runs/$t/RESULTS.txt
  [ "$t" = kimi ] && f=/Users/stevens/pi-problems-30/RESULTS.txt
  echo "----- $t -----"
  grep -E "P[0-9]+: (PASS|FAIL|STOP)" "$f" 2>/dev/null
done
