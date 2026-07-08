#!/bin/bash
# Generalized multi-model pi agent-loop harness.
# Usage: bash run_model.sh <provider> <model-id> <tag>
#   e.g. bash run_model.sh litellm-cherryrd cels/llama70 llama70
#        bash run_model.sh cels-chicago-4 nemotron-3-ultra nemotron
# Copies the pristine verifier scaffolding into runs/<tag>/, seeds the broken
# starting points, runs all 10 loops against the given model, writes
# runs/<tag>/RESULTS.txt. Verdicts come from verifier exit codes, never pi prose.

set -u
export PATH="/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
PI=/Users/stevens/.nvm/versions/node/v24.16.0/bin/pi
PY=/opt/anaconda3/bin/python3
PYTEST=/opt/anaconda3/bin/pytest

PROVIDER="$1"; MODEL="$2"; TAG="$3"
SRC=/Users/stevens/pi-problems-30          # pristine scaffolding (verifiers + seeds)
ROOT=/Users/stevens/pi-problems-30/runs/$TAG
PROV="--provider $PROVIDER --model $MODEL"
NS="--no-session -na"
RESULTS=$ROOT/RESULTS.txt

# --- HARD GUARD: refuse to run if any seed verifier passes pre-loop (contamination) ---
if [ -f "$SRC/assert_seeds_fail.sh" ]; then
  if ! bash "$SRC/assert_seeds_fail.sh" >/tmp/seedguard.$TAG.log 2>&1; then
    echo "ABORT: seed contamination guard FAILED -- see /tmp/seedguard.$TAG.log" >&2
    tail -5 /tmp/seedguard.$TAG.log >&2
    exit 3
  fi
fi

# --- SAFETY: never allow an empty TAG (would wipe all runs) ---
if [ -z "${TAG:-}" ]; then echo "ABORT: empty TAG" >&2; exit 4; fi
# Opt-in archival: set PI30_ARCHIVE=1 to append a timestamp suffix so a run is preserved
# instead of overwriting the stable tag. Default (unset) = stable tag (canonical, overwrite).
if [ "${PI30_ARCHIVE:-0}" = "1" ]; then
  TAG="${TAG}_$(date +%Y%m%d_%H%M%S)"
  echo "[archival] PI30_ARCHIVE=1 -> preserving run under timestamped tag: ${TAG}" >&2
fi

# --- stage a FRESH CLEAN directory for THIS run (wipe any prior same-tag run) ---
rm -rf "$ROOT"
mkdir -p "$ROOT"
# verify it is genuinely empty before staging
if [ -n "$(ls -A "$ROOT" 2>/dev/null)" ]; then echo "ABORT: $ROOT not clean after rm -rf" >&2; exit 5; fi
echo "[fresh-dir] clean run dir created: $ROOT" | tee -a "$RESULTS"
for p in p1 p2 p3 p4 p5 p6 p7 p8 p9 p10; do
  mkdir -p "$ROOT/$p"
  # copy only the verifier/seed/spec files, never prior generated artifacts
  # NOTE: never copy solution files (roman.py/fast.py/kernel.py/reduce.py/integrator.py/dispatch.py) --
  # they are the seed-contamination vector. Only verifier/scorer/spec files are staged.
  for f in verify.py check.py bench.py test_thing.py score.py converge_check.py PLAN.md; do
    [ -f "$SRC/$p/$f" ] && cp "$SRC/$p/$f" "$ROOT/$p/$f"
  done
done
: > "$RESULTS"

# Per-call hard timeout so a single hung pi agent-loop can't stall the whole run.
# 240s is generous for a 70B tool-loop; a hang gets SIGKILLed and the loop advances.
PITO="${PITO:-240}"
TIMEOUT="/opt/homebrew/bin/timeout -k 10 ${PITO}"
run_pi() { ( cd "$1" && $TIMEOUT "$PI" -p $PROV $NS "$2" ) >/dev/null 2>&1; }
record() { echo "$1" | tee -a "$RESULTS"; }

echo "==== $TAG ($MODEL) START $(date) ====" | tee -a "$RESULTS"

# P1
record "[P1] stats CLI"
run_pi "$ROOT/p1" "Write cli.py: reads whitespace/newline-separated numbers from STDIN, prints exactly one line 'count=N min=.. max=.. mean=.. median=.. stdev=..' (stdev = SAMPLE stdev, n-1). median of even count = avg of two middle. Stdlib only. Exit 0."
(cd "$ROOT/p1" && "$PY" verify.py) >/dev/null 2>&1 && record "P1: PASS" || record "P1: FAIL"

# P2
record "[P2] LRU cache + bundled tests"
run_pi "$ROOT/p2" "Implement lru.py with class LRUCache(capacity): get(key)->value-or-None, put(key,value), O(1), correct LRU eviction (get and put both count as use; put on existing key updates value AND refreshes recency). ALSO write test_lru.py with pytest tests and RUN pytest before done. Stdlib only."
(cd "$ROOT/p2" && "$PY" verify.py) >/dev/null 2>&1 && record "P2: PASS" || record "P2: FAIL"

# P3 iterate-until-green
record "[P3] Roman numerals iterate-until-green"
for i in $(seq 1 8); do
  (cd "$ROOT/p3" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P3: PASS green in $i"; break; }
  F=$(cd "$ROOT/p3" && "$PYTEST" -q test_thing.py 2>&1 | tail -n 25)
  run_pi "$ROOT/p3" "pytest test_thing.py failing. Fix roman.py to use subtractive notation (IV IX XL XC CD CM). Smallest fix. DO NOT edit test_thing.py. Failures:
$F"
  [ "$i" = 8 ] && record "P3: FAIL after 8"
done

# P4 oracle
record "[P4] stable softmax vs oracle"
for i in $(seq 1 6); do
  (cd "$ROOT/p4" && "$PY" check.py) >/dev/null 2>&1 && { record "P4: PASS in $i"; break; }
  O=$(cd "$ROOT/p4" && "$PY" check.py 2>&1 | tail -n 5)
  run_pi "$ROOT/p4" "fast.py softmax overflows / disagrees with reference in check.py. Fix for numerical stability (subtract max before exp). DO NOT edit check.py. Diagnostic:
$O"
  [ "$i" = 6 ] && record "P4: FAIL after 6"
done

# P5 measurement
record "[P5] matmul GFLOP/s"
best=0; stale=0; TARGET=5.0
for i in $(seq 1 8); do
  if ! (cd "$ROOT/p5" && "$PY" check.py) >/dev/null 2>&1; then
    O=$(cd "$ROOT/p5" && "$PY" check.py 2>&1 | tail -3)
    run_pi "$ROOT/p5" "kernel.matmul INCORRECT. Fix correctness (match numpy). DO NOT edit check.py/bench.py. $O"; continue
  fi
  g=$(cd "$ROOT/p5" && "$PY" bench.py --report 2>/dev/null); [ -z "$g" ] && g=0
  record "P5: round $i -> ${g} GFLOP/s"
  awk "BEGIN{exit !($g >= $TARGET)}" && { record "P5: PASS ${g} GFLOP/s"; break; }
  awk "BEGIN{exit !($g > $best)}" && { best=$g; stale=0; } || stale=$((stale+1))
  [ $stale -ge 3 ] && { record "P5: STOP plateau best=${best}"; break; }
  run_pi "$ROOT/p5" "kernel.matmul does ${g} GFLOP/s on 256x256 GEMM. Make ONE change to go faster (numpy vectorize / np.dot / @). Stay correct vs check.py. DO NOT edit check.py/bench.py."
  [ "$i" = 8 ] && record "P5: STOP budget best=${best}"
done

# P6 generator+critic
record "[P6] reproducible FP reduction"
P6=0
for i in $(seq 1 5); do
  run_pi "$ROOT/p6" "Improve reduce.py parallel_sum(xs,nchunks) so result is BIT-IDENTICAL regardless of nchunks. Address CRITIQUE.md if present. Hint: math.fsum over all data or a fixed ordering independent of nchunks. DO NOT edit verify.py."
  run_pi "$ROOT/p6" "HOSTILE reviewer fresh eyes: inspect reduce.py ONLY for dependence of result on nchunks / non-deterministic FP ordering. Write findings to CRITIQUE.md. If zero real issues write exactly NO_ISSUES on first line."
  if head -n1 "$ROOT/p6/CRITIQUE.md" 2>/dev/null | grep -q NO_ISSUES && (cd "$ROOT/p6" && "$PY" verify.py) >/dev/null 2>&1; then
    record "P6: PASS critic+verifier in $i"; P6=1; break; fi
done
[ "$P6" = 0 ] && { (cd "$ROOT/p6" && "$PY" verify.py) >/dev/null 2>&1 && record "P6: PASS verifier (critic not satisfied)" || record "P6: FAIL"; }

# P7 fan-out
record "[P7] parallel backends fan-out"
mkdir -p "$ROOT/p7/work"
for be in csv kv json; do
  ( mkdir -p "$ROOT/p7/work/$be" && cd "$ROOT/p7/work/$be" && \
    $TIMEOUT "$PI" -p $PROV $NS "Per ../../PLAN.md implement ONLY the '$be' backend in backend.py exposing parse(text)->dict. csv:'a,b,c'->{'fields':[...]}. kv:'k1=v1;k2=v2'->{'k1':'v1',...}. json: JSON object string -> dict via stdlib json. Stdlib only." ) >/dev/null 2>&1 &
done
wait
run_pi "$ROOT/p7" "Backends exist at work/{csv,kv,json}/backend.py each exposing parse(text)->dict. Write dispatch.py exposing dispatch(kind,text)->dict routing kind in {csv,kv,json}. Run verify.py. DO NOT edit verify.py."
(cd "$ROOT/p7" && "$PY" verify.py) >/dev/null 2>&1 && record "P7: PASS" || record "P7: FAIL"

# P8 reflection
record "[P8] ODE convergence + reflection"
MB=$(wc -c < /Users/stevens/.pi/agent/memory.md 2>/dev/null || echo 0)
for i in $(seq 1 6); do
  (cd "$ROOT/p8" && "$PY" converge_check.py) >/dev/null 2>&1 && { record "P8: PASS in $i"; break; }
  O=$(cd "$ROOT/p8" && "$PY" converge_check.py 2>&1 | tail -8)
  run_pi "$ROOT/p8" "integrator.solve fails converge_check.py. Use RK4 and compute t=t0+step*h (never accumulate). Append a one-line ROOT-CAUSE LESSON to ~/.pi/agent/memory.md. DO NOT edit converge_check.py. $O"
  [ "$i" = 6 ] && record "P8: FAIL after 6"
done
MA=$(wc -c < /Users/stevens/.pi/agent/memory.md 2>/dev/null || echo 0)
record "P8: memory.md ${MB}->${MA} bytes"

# P9 tournament
record "[P9] levenshtein tournament best-of-4"
mkdir -p "$ROOT/p9/arena"
for k in 1 2 3 4; do
  ( mkdir -p "$ROOT/p9/arena/cand_$k" && cd "$ROOT/p9/arena/cand_$k" && \
    $TIMEOUT "$PI" -p $PROV $NS "Write levenshtein.py exposing levenshtein(a,b)->int edit distance. CORRECT for all inputs incl empty, as FAST as possible (two-row DP, early exit). Stdlib only. Candidate #$k distinct angle." ) >/dev/null 2>&1 &
done
wait
best=""; bestf=0
for d in "$ROOT"/p9/arena/cand_*; do
  [ -f "$d/levenshtein.py" ] || continue
  f=$(cd "$ROOT/p9" && "$PY" score.py "$d/levenshtein.py" 2>/dev/null); [ -z "$f" ] && f=0
  record "P9: $(basename $d) score=${f}"
  awk "BEGIN{exit !($f > $bestf)}" && { bestf=$f; best=$d; }
done
[ -n "$best" ] && awk "BEGIN{exit !($bestf > 0)}" && record "P9: PASS champion=$(basename $best) @ ${bestf} kops/s" || record "P9: FAIL no correct candidate"

# P10 capstone
record "[P10] prime sieve capstone"
mkdir -p "$ROOT/p10/arena"
for k in 1 2 3; do
  ( mkdir -p "$ROOT/p10/arena/cand_$k" && cd "$ROOT/p10/arena/cand_$k" && \
    $TIMEOUT "$PI" -p $PROV $NS "Write sieve.py exposing primes_up_to(n)->sorted primes<=n. Correct for n<2 (empty), edge cases, FAST at n=2,000,000 (bytearray, skip evens, slice assign). Stdlib only. Candidate #$k distinct angle." ) >/dev/null 2>&1 &
done
wait
best=""; bestf=0
for d in "$ROOT"/p10/arena/cand_*; do
  [ -f "$d/sieve.py" ] || continue
  ( cd "$d" && $TIMEOUT "$PI" -p $PROV $NS "HOSTILE reviewer fresh eyes: inspect sieve.py for off-by-one (n included?), n<2, even bugs, slice-length bugs. If real bug, FIX sieve.py. Write VERDICT.txt: CLEAN or FIXED." ) >/dev/null 2>&1
  f=$(cd "$ROOT/p10" && "$PY" score.py "$d/sieve.py" 2>/dev/null); [ -z "$f" ] && f=0
  record "P10: $(basename $d) verdict=$(head -1 "$d/VERDICT.txt" 2>/dev/null) score=${f}"
  awk "BEGIN{exit !($f > $bestf)}" && { bestf=$f; best=$d; }
done
[ -n "$best" ] && awk "BEGIN{exit !($bestf > 0)}" && record "P10: PASS champion=$(basename $best) @ ${bestf} Mlimit/s" || record "P10: FAIL no correct candidate"

echo "==== $TAG DONE $(date) ====" | tee -a "$RESULTS"
echo "===== SUMMARY ($TAG / $MODEL) =====" | tee -a "$RESULTS"
grep -E "P[0-9]+: (PASS|FAIL|STOP)" "$RESULTS" | tee -a "$RESULTS"
