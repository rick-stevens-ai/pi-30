#!/bin/bash
# pi-30 fleet reporter: prints "which model is on which problem" from the heartbeat
# status dir. Used manually (cat) and by the 5-min Telegram cron.
SDIR=$(cat /tmp/pi30_fleet_status_dir.txt 2>/dev/null)
[ -z "$SDIR" ] || [ ! -d "$SDIR" ] && { echo "pi-30 fleet: no active run"; exit 0; }
echo "pi-30 FLEET status  $(date '+%H:%M:%S %Z')"
echo "----------------------------------------"
n=0; done=0
for f in "$SDIR"/*.cur; do
  [ -f "$f" ] || continue
  n=$((n+1))
  IFS='|' read -r model cur counts < "$f"
  printf '%-22s %-32s %s\n' "$model" "$cur" "$counts"
  echo "$cur" | grep -q DONE && done=$((done+1))
done
echo "----------------------------------------"
echo "$done/$n lanes complete"
[ -f "$SDIR/COMPLETE.txt" ] && echo ">> ALL DONE"
