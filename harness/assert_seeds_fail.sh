#!/bin/bash
# assert_seeds_fail.sh — pre-loop contamination guard for the pi vibe-coding curriculum.
# DOCTRINE: every seed MUST genuinely FAIL its verifier before any model loops.
# PASS-on-bare-seed = contamination (pre-solved arena) -> abort the sweep.
#
# Usage: bash assert_seeds_fail.sh            # all p1..p10 in-place
#        bash assert_seeds_fail.sh p1 p5      # subset
# Exit 0 = all clean; Exit 1 = contamination detected.
set -u
cd "$(dirname "$0")"
PY=/opt/anaconda3/bin/python3
PYTEST=/opt/anaconda3/bin/pytest
read -ra PROBS <<< "${*:-p1 p2 p3 p4 p5 p6 p7 p8 p9 p10}"

bad=0
check_cmd() { ( cd "$1" && shift && "$@" >/dev/null 2>&1 ); }

for p in "${PROBS[@]}"; do
  [ -d "$p" ] || { echo "$p: MISSING dir"; bad=1; continue; }
  case "$p" in
    p1|p2|p6|p7) cmd=($PY verify.py) ;;
    p3)          cmd=($PYTEST -q test_thing.py) ;;
    p4|p5)       cmd=($PY check.py) ;;
    p8)          cmd=($PY converge_check.py) ;;
    p9|p10)
      # Tournament: contamination = arena/ already holds a candidate that scores > 0.
      art=$( [ "$p" = p9 ] && echo levenshtein.py || echo sieve.py )
      hit=0
      if [ -d "$p/arena" ]; then
        for d in "$p"/arena/cand_*; do
          [ -f "$d/$art" ] || continue
          s=$(cd "$p" && $PY score.py "../$d/$art" 2>/dev/null); [ -z "$s" ] && s=0
          awk "BEGIN{exit !($s > 0)}" && { hit=1; break; }
        done
      fi
      if [ "$hit" = 1 ]; then echo "$p: CONTAMINATED (arena has a >0-scoring candidate before loop)"; bad=1
      else echo "$p: clean (no pre-scoring candidate in arena)"; fi
      continue ;;
    *) echo "$p: UNKNOWN verifier"; bad=1; continue ;;
  esac
  if check_cmd "$p" "${cmd[@]}"; then
    echo "$p: CONTAMINATED (verifier PASSES on bare seed — pre-solved!)"; bad=1
  else
    echo "$p: clean (verifier FAILS as required)"
  fi
done
echo '----'
if [ "$bad" = 0 ]; then echo 'ALL SEEDS CLEAN — safe to sweep.'; exit 0
else echo 'CONTAMINATION DETECTED — DO NOT SWEEP until decontaminated.'; exit 1; fi
