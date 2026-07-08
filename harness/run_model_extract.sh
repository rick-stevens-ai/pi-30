#!/bin/bash
# Code-extraction harness: works for ANY model (incl Ollama/spark) because it
# uses pi --no-tools and extracts the fenced code block, writing the artifact
# ourselves. Verdicts still come from verifier exit codes.
# Usage: bash run_model_extract.sh <provider> <model-id> <tag> [extra-pi-args]
#   e.g. bash run_model_extract.sh spark36 qwen3-coder:30b spark-qwen3coder --no-tools
set -u
export PATH="/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
PI=/Users/stevens/.nvm/versions/node/v24.16.0/bin/pi
PY=/opt/anaconda3/bin/python3
PYTEST=/opt/anaconda3/bin/pytest
EX=/Users/stevens/pi-problems-30/extract_code.py

PROVIDER="$1"; MODEL="$2"; TAG="$3"; shift 3
EXTRA="${*:---no-tools}"
SRC=/Users/stevens/pi-problems-30
ROOT=/Users/stevens/pi-problems-30/runs_extract/$TAG
RESULTS=$ROOT/RESULTS.txt
TMO=300   # per-call timeout (spark cold-loads are slow)
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout || true)"


rm -rf "$ROOT"; mkdir -p "$ROOT"
for p in p1 p2 p3 p4 p5 p11 p12 p13 p18 p23; do
  mkdir -p "$ROOT/$p"
  for f in verify.py check.py bench.py test_thing.py converge_check.py \
           roman.py fast.py kernel.py parens.py baseconv.py miniparse.py \
           stats.py primecount.py; do
    [ -f "$SRC/$p/$f" ] && cp "$SRC/$p/$f" "$ROOT/$p/$f"
  done
done
: > "$RESULTS"

# ask the model for a single fenced code block, extract -> artifact
gen() {  # gen <dir> <artifact> <prompt>
  local d="$1" art="$2" prompt="$3" raw="$1/.pi_out.txt"
  ( cd "$d" && ${TIMEOUT_BIN:+$TIMEOUT_BIN $TMO} "$PI" -p --provider "$PROVIDER" --model "$MODEL" $EXTRA \
      --no-session -na "$prompt
Respond with ONLY a single fenced python code block, no prose." ) > "$raw" 2>&1
  "$PY" "$EX" "$raw" "$d/$art" 2>/dev/null
}
record() { echo "$1" | tee -a "$RESULTS"; }

echo "==== EXTRACT $TAG ($MODEL) START $(date) ====" | tee -a "$RESULTS"

# P1 stats CLI
gen "$ROOT/p1" cli.py "Write cli.py: reads whitespace/newline-separated numbers from STDIN, prints exactly one line 'count=N min=.. max=.. mean=.. median=.. stdev=..' (stdev=SAMPLE n-1; median of even count = avg of two middle). Stdlib only."
(cd "$ROOT/p1" && "$PY" verify.py) >/dev/null 2>&1 && record "P1: PASS" || record "P1: FAIL"

# P2 LRU (single file, no bundled tests in extract mode)
gen "$ROOT/p2" lru.py "Write lru.py with class LRUCache(capacity): get(key)->value-or-None, put(key,value), O(1), correct LRU (get+put both count as use; put on existing key updates value AND refreshes recency). Stdlib only."
(cd "$ROOT/p2" && "$PY" verify.py) >/dev/null 2>&1 && record "P2: PASS" || record "P2: FAIL"

# P3 roman iterate-until-green
for i in $(seq 1 5); do
  (cd "$ROOT/p3" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P3: PASS green in $i"; break; }
  F=$(cd "$ROOT/p3" && "$PYTEST" -q test_thing.py 2>&1 | tail -20)
  CUR=$(cat "$ROOT/p3/roman.py" 2>/dev/null)
  gen "$ROOT/p3" roman.py "Fix roman.py so to_roman/from_roman use subtractive notation (IV IX XL XC CD CM) and round-trip 1..3999. Current code:
$CUR
pytest failures:
$F"
  [ "$i" = 5 ] && record "P3: FAIL after 5"
done

# P4 softmax oracle
for i in $(seq 1 4); do
  (cd "$ROOT/p4" && "$PY" check.py) >/dev/null 2>&1 && { record "P4: PASS in $i"; break; }
  O=$(cd "$ROOT/p4" && "$PY" check.py 2>&1 | tail -5)
  gen "$ROOT/p4" fast.py "Write fast.py with softmax(xs)->list that is numerically stable (subtract max before exp), sums to 1, no overflow on large logits like 800. Diagnostic from checker:
$O"
  [ "$i" = 4 ] && record "P4: FAIL after 4"
done

# P5 matmul measurement
best=0; stale=0; TARGET=5.0
for i in $(seq 1 5); do
  if ! (cd "$ROOT/p5" && "$PY" check.py) >/dev/null 2>&1; then
    gen "$ROOT/p5" kernel.py "Write kernel.py with matmul(A,B) that matches numpy (use numpy @ / np.dot, return array-like). Must be correct for square matrices."
    continue
  fi
  g=$(cd "$ROOT/p5" && "$PY" bench.py --report 2>/dev/null); [ -z "$g" ] && g=0
  record "P5: round $i -> ${g} GFLOP/s"
  awk "BEGIN{exit !($g >= $TARGET)}" && { record "P5: PASS ${g} GFLOP/s"; break; }
  awk "BEGIN{exit !($g > $best)}" && { best=$g; stale=0; } || stale=$((stale+1))
  [ $stale -ge 2 ] && { record "P5: STOP plateau best=${best}"; break; }
  gen "$ROOT/p5" kernel.py "Write kernel.py matmul(A,B) as FAST as possible using numpy (np.asarray then @). Must match numpy. Current GFLOP/s=${g}."
  [ "$i" = 5 ] && record "P5: STOP budget best=${best}"
done

# P11 balanced parens iterate-until-green
for i in $(seq 1 4); do
  (cd "$ROOT/p11" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P11: PASS green in $i"; break; }
  F=$(cd "$ROOT/p11" && "$PYTEST" -q test_thing.py 2>&1 | tail -15)
  gen "$ROOT/p11" parens.py "Write parens.py with is_balanced(s)->bool that validates (), [], {} matching using a stack, ignoring other chars. pytest failures:
$F"
  [ "$i" = 4 ] && record "P11: FAIL after 4"
done

# P12 base-N oracle
for i in $(seq 1 4); do
  (cd "$ROOT/p12" && "$PY" check.py) >/dev/null 2>&1 && { record "P12: PASS in $i"; break; }
  O=$(cd "$ROOT/p12" && "$PY" check.py 2>&1 | tail -4)
  gen "$ROOT/p12" baseconv.py "Write baseconv.py with to_base(n,base)->lowercase string and parse_int(s,base)->int for base 2..36, round-tripping and matching int(s,base). Diagnostic:
$O"
  [ "$i" = 4 ] && record "P12: FAIL after 4"
done

# P13 mini json parser iterate-until-green
for i in $(seq 1 5); do
  (cd "$ROOT/p13" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P13: PASS green in $i"; break; }
  F=$(cd "$ROOT/p13" && "$PYTEST" -q test_thing.py 2>&1 | tail -15)
  gen "$ROOT/p13" miniparse.py "Write miniparse.py with parse(s) that parses a JSON subset (null/true/false/int/float/string/array/object, nesting, whitespace) WITHOUT using the json module or eval. pytest failures:
$F"
  [ "$i" = 5 ] && record "P13: FAIL after 5"
done

# P18 welford reflection (no memory write in extract mode)
for i in $(seq 1 4); do
  (cd "$ROOT/p18" && "$PY" converge_check.py) >/dev/null 2>&1 && { record "P18: PASS in $i"; break; }
  O=$(cd "$ROOT/p18" && "$PY" converge_check.py 2>&1 | tail -6)
  gen "$ROOT/p18" stats.py "Write stats.py with running_variance(data)->sample variance (n-1) using Welford's online algorithm (numerically stable, no catastrophic cancellation, handles constant streams as 0). Diagnostic:
$O"
  [ "$i" = 4 ] && record "P18: FAIL after 4"
done

# P23 prime-count measurement
best=0; stale=0; TARGET=8.0
for i in $(seq 1 5); do
  if ! (cd "$ROOT/p23" && "$PY" check.py) >/dev/null 2>&1; then
    gen "$ROOT/p23" primecount.py "Write primecount.py with count_primes(n)->number of primes below n, CORRECT for small n."
    continue
  fi
  g=$(cd "$ROOT/p23" && "$PY" bench.py --report 2>/dev/null); [ -z "$g" ] && g=0
  record "P23: round $i -> ${g} Mn/s"
  awk "BEGIN{exit !($g >= $TARGET)}" && { record "P23: PASS ${g} Mn/s"; break; }
  awk "BEGIN{exit !($g > $best)}" && { best=$g; stale=0; } || stale=$((stale+1))
  [ $stale -ge 2 ] && { record "P23: STOP plateau best=${best}"; break; }
  gen "$ROOT/p23" primecount.py "Write primecount.py count_primes(n) as FAST as possible using a Sieve of Eratosthenes with bytearray. Must be correct. Current Mn/s=${g}."
  [ "$i" = 5 ] && record "P23: STOP budget best=${best}"
done

echo "==== $TAG DONE $(date) ====" | tee -a "$RESULTS"
# build summary WITHOUT appending duplicate P-lines back into RESULTS (avoids double-count)
{ echo "===== SUMMARY ($TAG / $MODEL) ====="
  grep -E "^P[0-9]+: (PASS|FAIL|STOP)" "$RESULTS"
  PASS=$(grep -cE "^P[0-9]+: PASS" "$RESULTS")
  echo "SCORE: $PASS/10 passed"
} > "$ROOT/SUMMARY.txt"
cat "$ROOT/SUMMARY.txt"
