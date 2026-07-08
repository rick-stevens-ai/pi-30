#!/bin/bash
# Resume-mode OpenRouter backoff re-run of the two gpt-oss lanes, 24h cap.
# Runs both lanes in PI30_RESUME mode against the existing run dirs so only
# not-yet-PASSed problems are re-attempted, routed through the m1:8898 backoff proxy.
set -u
export PATH="/opt/homebrew/bin:/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
cd /Users/stevens/pi-problems-30

DEADLINE=$(( $(date +%s) + 24*3600 ))   # 24h from now
STATUS=/Users/stevens/pi-problems-30/or_backoff_status.txt

# Longer per-call timeout: backoff can legitimately take up to ~5 min on bad bursts.
export PI_TIMEOUT=420
export PI30_RESUME=1

run_lane() {
  local prov="$1" model="$2" tag="$3"
  local log="sweep_logs/${tag}.orbackoff.log"
  # Loop: keep resuming this lane until all 30 done OR deadline hit.
  while [ "$(date +%s)" -lt "$DEADLINE" ]; do
    bash run_model_30.sh "$prov" "$model" "$tag" >> "$log" 2>&1
    # Count remaining TODO
    local todo
    todo=$(/opt/anaconda3/bin/python3 - "runs30/$tag/RESULTS.txt" <<'PY'
import sys,re
last={}
try:
    for ln in open(sys.argv[1]):
        m=re.match(r"(P\d+):\s+(PASS|FAIL)",ln)
        if m: last[m.group(1)]=m.group(2)
except FileNotFoundError:
    pass
print(sum(1 for i in range(1,31) if last.get(f"P{i}")!="PASS"))
PY
)
    echo "$(date '+%H:%M:%S') $tag pass-remaining=$todo" >> "$STATUS"
    [ "$todo" = "0" ] && break
    sleep 30
  done
}

: > "$STATUS"
echo "$(date '+%Y-%m-%d %H:%M:%S') START 24h backoff re-run; deadline=$(date -r $DEADLINE '+%H:%M %Z')" >> "$STATUS"
run_lane or-backoff openai/gpt-oss-120b:free oss120-openrouter-20260706-0751 &
P1=$!
run_lane or-backoff openai/gpt-oss-20b:free  oss20b-openrouter-20260706-0754 &
P2=$!
wait $P1 $P2
echo "$(date '+%Y-%m-%d %H:%M:%S') ALL LANES FINISHED (or deadline)" >> "$STATUS"
