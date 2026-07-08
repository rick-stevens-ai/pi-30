#!/bin/bash
# Master driver: 10 pi+kimi-k2.6 agent-loop problems (method ladder L1-L10).
# Each problem has a machine-checkable verifier the agent never edits.
# Verdicts come from exit codes / files, never from the model's prose.

export PATH="/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
PI=/Users/stevens/.nvm/versions/node/v24.16.0/bin/pi
PY=/opt/anaconda3/bin/python3
PYTEST=/opt/anaconda3/bin/pytest
PROV="--provider litellm-cherryrd --model cels/kimi-k2.6"
NS="--no-session -na"

ROOT=/Users/stevens/pi-problems-30
RESULTS=$ROOT/RESULTS.txt
: > "$RESULTS"

run_pi() {  # run_pi <dir> <prompt>
  ( cd "$1" && "$PI" -p $PROV $NS "$2" ) >/dev/null 2>&1
}
record() { echo "$1" | tee -a "$RESULTS"; }

echo "==== START $(date) ===="

# ---------- P1 L1: single-shot utility ----------
record "[P1 L1] single-shot stats CLI"
rm -f "$ROOT/p1/cli.py"
run_pi "$ROOT/p1" "Write cli.py: a stats tool that reads whitespace/newline-separated numbers from STDIN and prints exactly one line: 'count=N min=.. max=.. mean=.. median=.. stdev=..' where stdev is the SAMPLE standard deviation (n-1 denominator). median of even count = average of two middle values. Use only the Python stdlib. Exit 0."
if (cd "$ROOT/p1" && "$PY" verify.py) >/tmp/p1.log 2>&1; then record "P1: PASS"; else record "P1: FAIL ($(tail -1 /tmp/p1.log))"; fi

# ---------- P2 L2: generate + bundled tests ----------
record "[P2 L2] LRU cache + bundled tests"
rm -f "$ROOT/p2/lru.py" "$ROOT/p2/test_lru.py"
run_pi "$ROOT/p2" "Implement lru.py with class LRUCache(capacity): methods get(key)->value-or-None and put(key,value), O(1), correct LRU eviction (get and put both count as 'use'; put on existing key updates value AND refreshes recency). ALSO write test_lru.py with thorough pytest tests and RUN pytest yourself before declaring done. Stdlib only."
if (cd "$ROOT/p2" && "$PY" verify.py) >/tmp/p2.log 2>&1; then record "P2: PASS (independent verifier)"; else record "P2: FAIL ($(tail -1 /tmp/p2.log))"; fi
if (cd "$ROOT/p2" && "$PYTEST" -q test_lru.py) >/tmp/p2t.log 2>&1; then record "P2: agent's own tests green"; else record "P2: agent's own tests RED/absent"; fi

# ---------- P3 L3: iterate-until-green ----------
record "[P3 L3] Roman numerals iterate-until-green"
for i in $(seq 1 8); do
  if (cd "$ROOT/p3" && "$PYTEST" -q test_thing.py) >/tmp/p3.log 2>&1; then
    record "P3: PASS green in $i iteration(s)"; break; fi
  FAILS=$(cd "$ROOT/p3" && "$PYTEST" -q test_thing.py 2>&1 | tail -n 30)
  run_pi "$ROOT/p3" "pytest on test_thing.py is failing. Fix roman.py (to_roman/from_roman) to use proper subtractive notation (IV, IX, XL, XC, CD, CM). Make the SMALLEST fix. DO NOT edit test_thing.py. Failures:
$FAILS"
  [ "$i" = 8 ] && record "P3: FAIL after 8 iterations"
done

# ---------- P4 L4: differential / oracle ----------
record "[P4 L4] numerically-stable softmax vs oracle"
for i in $(seq 1 6); do
  if (cd "$ROOT/p4" && "$PY" check.py) >/tmp/p4.log 2>&1; then
    record "P4: PASS matches oracle in $i ($(tail -1 /tmp/p4.log))"; break; fi
  OUT=$(cd "$ROOT/p4" && "$PY" check.py 2>&1 | tail -n 5)
  run_pi "$ROOT/p4" "fast.py's softmax disagrees with the high-precision reference in check.py and/or overflows on large logits. Fix fast.py for numerical stability (subtract the max before exp). DO NOT edit check.py. Diagnostic:
$OUT"
  [ "$i" = 6 ] && record "P4: FAIL after 6 iterations"
done

# ---------- P5 L5: measurement-in-the-loop ----------
record "[P5 L5] matmul GFLOP/s optimization"
best=0; stale=0; TARGET=5.0
for i in $(seq 1 8); do
  if ! (cd "$ROOT/p5" && "$PY" check.py) >/tmp/p5c.log 2>&1; then
    OUT=$(cd "$ROOT/p5" && "$PY" check.py 2>&1 | tail -3)
    run_pi "$ROOT/p5" "kernel.matmul is INCORRECT. Fix correctness first (must match numpy). DO NOT edit check.py/bench.py. $OUT"
    continue
  fi
  g=$(cd "$ROOT/p5" && "$PY" bench.py --report 2>/dev/null)
  [ -z "$g" ] && g=0
  record "P5: round $i -> ${g} GFLOP/s (best ${best})"
  if awk "BEGIN{exit !($g >= $TARGET)}"; then record "P5: PASS hit target ${g} GFLOP/s"; break; fi
  if awk "BEGIN{exit !($g > $best)}"; then best=$g; stale=0; else stale=$((stale+1)); fi
  if [ $stale -ge 3 ]; then record "P5: STOP plateau at best=${best} GFLOP/s"; break; fi
  run_pi "$ROOT/p5" "kernel.matmul currently does ${g} GFLOP/s on a 256x256 GEMM (bench.py). Make ONE change to go faster (vectorize with numpy, use np.dot/@ on contiguous arrays, or block). MUST stay correct vs check.py (run: $PY check.py). DO NOT edit check.py/bench.py."
  [ "$i" = 8 ] && record "P5: STOP iteration budget (best=${best})"
done

# ---------- P6 L6: generator + critic ----------
record "[P6 L6] reproducible FP reduction (generator+critic)"
P6PASS=0
for i in $(seq 1 5); do
  run_pi "$ROOT/p6" "Improve reduce.py parallel_sum(xs,nchunks) so the result is BIT-IDENTICAL regardless of nchunks (FP addition is non-associative). Address every open item in CRITIQUE.md if it exists. Hint: a canonical summation (math.fsum over the whole data, or a fixed deterministic ordering independent of nchunks) fixes it. DO NOT edit verify.py."
  run_pi "$ROOT/p6" "You are a HOSTILE reviewer with FRESH eyes. Inspect reduce.py ONLY for: dependence of the result on nchunks, non-deterministic FP ordering, accidental use of nchunks in the math. Write findings to CRITIQUE.md as a checklist. If and ONLY IF there are zero real issues, write exactly NO_ISSUES on the first line."
  if head -n1 "$ROOT/p6/CRITIQUE.md" 2>/dev/null | grep -q NO_ISSUES; then
    if (cd "$ROOT/p6" && "$PY" verify.py) >/tmp/p6.log 2>&1; then
      record "P6: PASS critic satisfied + verifier green in $i ($(tail -1 /tmp/p6.log))"; P6PASS=1; break
    else
      record "P6: critic said NO_ISSUES but verifier FAILED — continuing"
    fi
  fi
done
[ "$P6PASS" = 0 ] && { (cd "$ROOT/p6" && "$PY" verify.py) >/tmp/p6.log 2>&1 && record "P6: PASS verifier green (critic not fully satisfied)" || record "P6: FAIL ($(tail -1 /tmp/p6.log))"; }

# ---------- P7 L7: plan -> fan-out -> integrate ----------
record "[P7 L7] parallel backends fan-out + integrate"
rm -rf "$ROOT/p7/work" "$ROOT/p7/dispatch.py"
mkdir -p "$ROOT/p7/work"
for be in csv kv json; do
  ( mkdir -p "$ROOT/p7/work/$be" && cd "$ROOT/p7/work/$be" && \
    "$PI" -p $PROV $NS "Per ../../PLAN.md, implement ONLY the '$be' backend in backend.py exposing parse(text)->dict. csv: 'a,b,c'->{'fields':[...]}. kv: 'k1=v1;k2=v2'->{'k1':'v1',...}. json: a JSON object string -> the dict via stdlib json. Stdlib only. Also write a tiny test_backend.py proving it." ) >"$ROOT/p7/work/$be/worker.log" 2>&1 &
done
wait
record "P7: workers done; backends present: $(ls "$ROOT"/p7/work/*/backend.py 2>/dev/null | wc -l | tr -d ' ')/3"
run_pi "$ROOT/p7" "All three backends exist at work/csv/backend.py, work/kv/backend.py, work/json/backend.py, each exposing parse(text)->dict. Write dispatch.py exposing dispatch(kind,text)->dict that imports those backend modules and routes kind in {'csv','kv','json'} to the right one. Run verify.py to confirm. DO NOT edit verify.py."
if (cd "$ROOT/p7" && "$PY" verify.py) >/tmp/p7.log 2>&1; then record "P7: PASS"; else record "P7: FAIL ($(tail -1 /tmp/p7.log))"; fi

# ---------- P8 L8: reflection / self-improvement ----------
record "[P8 L8] ODE integrator convergence + memory reflection"
MEMBEFORE=$(wc -c < /Users/stevens/.pi/agent/memory.md 2>/dev/null || echo 0)
for i in $(seq 1 6); do
  if (cd "$ROOT/p8" && "$PY" converge_check.py) >/tmp/p8.log 2>&1; then
    record "P8: PASS converged in $i ($(tail -1 /tmp/p8.log))"; break; fi
  OUT=$(cd "$ROOT/p8" && "$PY" converge_check.py 2>&1 | tail -n 8)
  run_pi "$ROOT/p8" "integrator.solve fails converge_check.py. 1) Fix it: use RK4 (4th order) and compute t as t0+step*h (NEVER accumulate t+=h). 2) Append a one-line ROOT-CAUSE LESSON to ~/.pi/agent/memory.md. DO NOT edit converge_check.py. Diagnostic:
$OUT"
  [ "$i" = 6 ] && record "P8: FAIL after 6 iterations"
done
MEMAFTER=$(wc -c < /Users/stevens/.pi/agent/memory.md 2>/dev/null || echo 0)
record "P8: memory.md grew ${MEMBEFORE} -> ${MEMAFTER} bytes (reflection $([ "$MEMAFTER" -gt "$MEMBEFORE" ] && echo recorded || echo NOT-recorded))"

# ---------- P9 L9: tournament / best-of-N ----------
record "[P9 L9] levenshtein tournament best-of-4"
rm -rf "$ROOT/p9/arena"; mkdir -p "$ROOT/p9/arena"
for k in 1 2 3 4; do
  ( mkdir -p "$ROOT/p9/arena/cand_$k" && cd "$ROOT/p9/arena/cand_$k" && \
    "$PI" -p $PROV $NS "Write levenshtein.py exposing levenshtein(a,b)->int (edit distance). Be CORRECT for all inputs incl empty strings, and as FAST as you can (two-row DP, early exit when strings equal, etc). Stdlib only. Candidate #$k — try a distinct optimization angle." ) >"$ROOT/p9/arena/cand_$k/w.log" 2>&1 &
done
wait
best=""; bestf=0
for d in "$ROOT"/p9/arena/cand_*; do
  [ -f "$d/levenshtein.py" ] || { record "P9: $(basename $d) no artifact"; continue; }
  f=$(cd "$ROOT/p9" && "$PY" score.py "$d/levenshtein.py" 2>/dev/null)
  [ -z "$f" ] && f=0
  record "P9: $(basename $d) score=${f} kops/s"
  if awk "BEGIN{exit !($f > $bestf)}"; then bestf=$f; best=$d; fi
done
if [ -n "$best" ] && awk "BEGIN{exit !($bestf > 0)}"; then
  cp "$best/levenshtein.py" "$ROOT/p9/champion.py"
  record "P9: PASS champion=$(basename $best) @ ${bestf} kops/s"
else
  record "P9: FAIL no correct candidate"
fi

# ---------- P10 L10: capstone (tournament + critic + benchmark) ----------
record "[P10 L10] prime sieve capstone (tournament+critic+bench)"
rm -rf "$ROOT/p10/arena"; mkdir -p "$ROOT/p10/arena"
for k in 1 2 3; do
  ( mkdir -p "$ROOT/p10/arena/cand_$k" && cd "$ROOT/p10/arena/cand_$k" && \
    "$PI" -p $PROV $NS "Write sieve.py exposing primes_up_to(n)->sorted list of primes <= n. Correct for n<2 (empty), edge cases, and as FAST as possible at n=2,000,000 (sieve of Eratosthenes with bytearray, skip evens, slice assignment). Stdlib only. Candidate #$k distinct angle." ) >"$ROOT/p10/arena/cand_$k/w.log" 2>&1 &
done
wait
# critic pass: each candidate gets a hostile review; only reviewed-clean ones compete
best=""; bestf=0
for d in "$ROOT"/p10/arena/cand_*; do
  [ -f "$d/sieve.py" ] || { record "P10: $(basename $d) no artifact"; continue; }
  ( cd "$d" && "$PI" -p $PROV $NS "HOSTILE reviewer, fresh eyes: inspect sieve.py for off-by-one (is n itself included?), n<2 handling, even-number bugs, slice-length bugs. If you find a real bug, FIX sieve.py directly. Then write VERDICT.txt: 'CLEAN' if no issues remain, else 'FIXED'." ) >"$d/critic.log" 2>&1
  f=$(cd "$ROOT/p10" && "$PY" score.py "$d/sieve.py" 2>/dev/null)
  [ -z "$f" ] && f=0
  record "P10: $(basename $d) verdict=$(head -1 "$d/VERDICT.txt" 2>/dev/null) score=${f} Mlimit/s"
  if awk "BEGIN{exit !($f > $bestf)}"; then bestf=$f; best=$d; fi
done
if [ -n "$best" ] && awk "BEGIN{exit !($bestf > 0)}"; then
  cp "$best/sieve.py" "$ROOT/p10/champion.py"
  record "P10: PASS champion=$(basename $best) @ ${bestf} Mlimit/s"
else
  record "P10: FAIL no correct candidate"
fi

echo "==== DONE $(date) ===="
echo "" | tee -a "$RESULTS"
echo "===== SUMMARY =====" | tee -a "$RESULTS"
grep -E "P[0-9]+: (PASS|FAIL|STOP)" "$RESULTS" | tee -a "$RESULTS"
