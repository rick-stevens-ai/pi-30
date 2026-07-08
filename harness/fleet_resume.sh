#!/opt/homebrew/bin/bash
# Resume the pi-30 fleet lanes killed by the SIGTERM cascade. Each lane is launched
# into its OWN session via setsid_shim.py (macOS has no setsid) so a SIGTERM to this
# launcher / the Hermes bg-wrapper CANNOT cascade-kill the lanes. Lanes run under
# homebrew bash 5 (resume path uses `declare -A`, needs bash 4+; /bin/bash is 3.2).
# Resume = PI30_RESUME reads runs30/<tag>/RESULTS.txt.prior, skips prior PASSes.
# NO pid-heartbeat: a separate reporter reads RESULTS.txt directly.
set -u
SRC=/Users/stevens/pi-problems-30
PROVIDER=chiatta00-agg
SHIM="$SRC/setsid_shim.py"

LANES=(
  "gemma4-12b:fleet-gemma4-12b-20260705-2040"
  "gemma4-31b:fleet-gemma4-31b-20260705-2040"
  "ornith-9b:fleet-ornith-9b-20260705-2040"
  "qwen36-27b:fleet-qwen36-27b-20260705-2040"
  "uic-gemma4-26b-q8:fleet-uic-gemma4-26b-q8-20260705-2040"
  "uic-gemma4-26b-q4:fleet-uic-gemma4-26b-q4-20260705-2040"
)

for pair in "${LANES[@]}"; do
  m="${pair%%:*}"; tag="${pair##*:}"
  log="$SRC/runs30_${tag}.resume.log"
  PI30_RESUME=1 PI_TIMEOUT=360 /usr/bin/python3 "$SHIM" \
      /opt/homebrew/bin/bash "$SRC/run_model_30.sh" "$PROVIDER" "$m" "$tag" > "$log" 2>&1
  echo "launched $m ($tag) -> $log"
  sleep 1
done
echo "resumed ${#LANES[@]} lanes $(date) — detached, launcher exiting"
