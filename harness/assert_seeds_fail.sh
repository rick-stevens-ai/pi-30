#!/bin/bash
# assert_seeds_fail.sh — pre-loop contamination guard for the pi vibe-coding curriculum.
# DOCTRINE: every seed MUST genuinely FAIL its verifier before any model loops.
# PASS-on-bare-seed = contamination (pre-solved arena) -> abort the sweep.
#
# Usage: bash assert_seeds_fail.sh            # all p1..p30 (auto-locates problems/)
#        bash assert_seeds_fail.sh p1 p5      # subset
# Exit 0 = all clean; Exit 1 = contamination detected.
set -u
# Locate the problems directory: prefer ../problems (repo layout), else cwd/in-place.
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(dirname "$HERE")"
if [ -d "$REPO/problems/p1" ]; then
  cd "$REPO/problems"
elif [ -d "./p1" ]; then
  :  # problem dirs already in cwd (legacy in-place layout)
else
  cd "$HERE"
fi
# Python/pytest: honor PI30_PY/PI30_PYTEST overrides, else fall back to PATH.
PY="${PI30_PY:-$(command -v python3 || echo /opt/anaconda3/bin/python3)}"
PYTEST="${PI30_PYTEST:-$PY -m pytest}"
read -ra PROBS <<< "${*:-p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 p16 p17 p18 p19 p20 p21 p22 p23 p24 p25 p26 p27 p28 p29 p30}"

bad=0
check_cmd() { ( cd "$1" && shift && "$@" >/dev/null 2>&1 ); }

for p in "${PROBS[@]}"; do
  [ -d "$p" ] || { echo "$p: MISSING dir"; bad=1; continue; }
  case "$p" in
    p1|p2|p6|p7|p16|p17|p24|p25) cmd=($PY verify.py) ;;
    p3|p11|p13|p20|p22|p29)      cmd=($PYTEST -q test_thing.py) ;;
    p4|p12|p14|p21|p28)          cmd=($PY check.py) ;;
    p5|p15|p23)
      # OPTIMIZE task: the seed is intentionally CORRECT but SLOW. Correctness
      # (check.py) legitimately passes; the challenge is the bench THROUGHPUT target.
      # bench.py only PRINTS the metric (it does not exit-gate on the target), so we
      # compare the reported metric against the task target (same values as the
      # reference harness run_model_30.sh). Contamination = seed already >= target.
      case "$p" in p5) tgt=5.0 ;; p15) tgt=1.0 ;; p23) tgt=8.0 ;; esac
      if ! check_cmd "$p" $PY check.py; then
        echo "$p: clean (optimize seed not yet correct — will be fixed+sped up)"; continue; fi
      metric=$(cd "$p" && $PY bench.py --report 2>/dev/null | head -1); [ -z "$metric" ] && metric=0
      if awk "BEGIN{exit !($metric >= $tgt)}"; then
        echo "$p: CONTAMINATED (optimize seed metric $metric already >= target $tgt — pre-optimized!)"; bad=1
      else
        echo "$p: clean (metric $metric below target $tgt, as required)"
      fi
      continue ;;
    p8|p18|p26)                  cmd=($PY converge_check.py) ;;
    p9|p10|p19|p27|p30)
      # Tournament: contamination = arena/ already holds a candidate that scores > 0.
      case "$p" in
        p9)  art=levenshtein.py ;;
        p10) art=sieve.py ;;
        p19) art=fib.py ;;
        p27) art=substr.py ;;
        p30) art=sortkernel.py ;;
      esac
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
