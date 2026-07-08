#!/bin/bash
# pi-30 FLEET parallel launcher (2026-07-05).
# Runs all 13 chiatta00-agg models through the full 30-problem harness IN PARALLEL,
# one lane per model. Each lane writes a heartbeat (current problem) so a reporter
# can list "which model is on which problem" every 5 min. Full coverage: every
# model x every problem. Harness = run_model_30.sh (unchanged, tested).
set -u
SRC=/Users/stevens/pi-problems-30
STAMP=$(date +%Y%m%d-%H%M)
STATUS=$SRC/fleet_status_$STAMP
mkdir -p "$STATUS"
echo "$STATUS" > /tmp/pi30_fleet_status_dir.txt

PROVIDER=chiatta00-agg
MODELS=(gemma4-e2b gemma4-e4b gemma4-12b gemma4-31b ornith-9b devstral-small-2 \
        qwen36-27b uic-ornith-9b uic-ornith-35b uic-gemma4-26b-q8 uic-gemma4-26b-q4 \
        uic-laguna-xs2 uic-qwen36-35b-a3b)

# Heartbeat wrapper: tails a lane's RESULTS.txt and writes the latest [Pn] marker
# to $STATUS/<model>.cur every few seconds while the lane runs.
heartbeat() {
  local model="$1" tag="$2" pid="$3"
  local res="$SRC/runs30/$tag/RESULTS.txt"
  while kill -0 "$pid" 2>/dev/null; do
    if [ -f "$res" ]; then
      local last; last=$(grep -oE '\[P[0-9]+\][^]]*' "$res" | tail -1)
      local np;   np=$(grep -c ': PASS' "$res")
      local nf;   nf=$(grep -c ': FAIL' "$res")
      printf '%s|%s|pass=%s fail=%s\n' "$model" "${last:-starting}" "$np" "$nf" > "$STATUS/$model.cur"
    else
      printf '%s|(staging)|pass=0 fail=0\n' "$model" > "$STATUS/$model.cur"
    fi
    sleep 5
  done
  # final line
  if [ -f "$res" ]; then
    local np nf; np=$(grep -c ': PASS' "$res"); nf=$(grep -c ': FAIL' "$res")
    printf '%s|DONE|pass=%s fail=%s\n' "$model" "$np" "$nf" > "$STATUS/$model.cur"
  fi
}

for m in "${MODELS[@]}"; do
  tag="fleet-$m-$STAMP"
  # sanitize tag (dir-safe)
  tag="${tag//\//_}"
  log="$SRC/runs30_${tag}.log"
  # setsid: detach each lane into its OWN session/process-group so a SIGTERM to
  # this launcher (or the Hermes bg-process wrapper) does NOT cascade-kill the
  # lanes. PI30_RESUME=1: skip problems already recorded PASS (continue partials).
  PI30_RESUME=1 PI_TIMEOUT=360 setsid bash "$SRC/run_model_30.sh" "$PROVIDER" "$m" "$tag" > "$log" 2>&1 &
  lanepid=$!
  echo "$m $tag $lanepid" >> "$STATUS/lanes.txt"
  setsid bash -c "$(declare -f heartbeat); SRC='$SRC' STATUS='$STATUS' heartbeat '$m' '$tag' '$lanepid'" &
done
echo "launched ${#MODELS[@]} lanes at $STAMP" 
wait
echo "ALL LANES DONE $(date)" > "$STATUS/COMPLETE.txt"
