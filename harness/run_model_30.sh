#!/bin/bash
# 30-problem pi agent-loop harness (tool-use). Extends run_model.sh (P1-P10) with
# authored P11-P30 blocks. Verdicts come from verifier EXIT CODES, never pi prose.
# Usage: bash run_model_30.sh <provider> <model-id> <tag>
#   e.g. bash run_model_30.sh ds4 deepseek-v4-flash ds4-flash
set -u
# --- environment hygiene (2026-07-04) -----------------------------------------
# The user's shell exports PYTHONPATH=~/Library/Python/3.9/site-packages, which
# contains a bare py.py that SHADOWS the real `py` package. anaconda's pytest
# 6.2.4 does `from py.test import console_main` -> imports that py.py -> crashes
# ("No module named 'py.test'; 'py' is not a package"). Result: EVERY pytest-based
# problem (P3/P11/P13/P20/P22 + more, 12 call sites) auto-FAILED for ALL models
# regardless of output -> false 0/N lanes. The same leak also breaks the newer
# urllib3 (tuple[...] subscripts) that anaconda's py3.8 conda imports, spamming a
# conda crash into every login shell the pi bash-tool spawns. Scrubbing PYTHONPATH
# fixes both: pytest works, conda init stops crashing. Verified 2026-07-04.
unset PYTHONPATH
export CONDA_NO_PLUGINS=true
export PATH="/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
PI=/Users/stevens/.nvm/versions/node/v24.16.0/bin/pi
PY=/opt/anaconda3/bin/python3
PYTEST=/opt/anaconda3/bin/pytest

# --- per-pi-call timeout guard ---------------------------------------------
# A single stalled endpoint request (pi has NO internal request timeout) can
# wedge a whole sequential lane indefinitely (nemotron/chicago-4 hung 11h on
# P26, 2026-07-03). Every pi invocation goes through gtimeout so a hung call
# is killed and becomes a clean FAIL instead of blocking the lane forever.
# Override per run:  PI_TIMEOUT=600 bash run_model_30.sh ...
GT=$(command -v gtimeout || command -v timeout)
PI_TIMEOUT="${PI_TIMEOUT:-300}"        # seconds per single pi call
# -k 15: if pi ignores SIGTERM, SIGKILL 15s later. gtimeout exit 124 = timed out.
PT="$GT -k 15 $PI_TIMEOUT $PI"
[ -z "$GT" ] && { echo "FATAL: no gtimeout/timeout on PATH — install coreutils"; exit 2; }

# --- per-score.py timeout guard --------------------------------------------
# score.py imports the candidate module and runs my_sort/etc IN-PROCESS. A
# candidate with an infinite loop or pathological runtime (e.g. ornith-9b's
# broken radix sort on P30, 2026-07-06, wedged a lane 6.5h) would hang the whole
# sequential lane forever. Wrap every score.py call in gtimeout so a bad kernel
# is SIGKILLed and scores 0 (empty stdout -> f=0 -> candidate simply loses).
SCORE_TIMEOUT="${SCORE_TIMEOUT:-120}"   # seconds per candidate benchmark
SC="$GT -k 5 $SCORE_TIMEOUT"

PROVIDER="$1"; MODEL="$2"; TAG="$3"
SRC=/Users/stevens/pi-problems-30
ROOT=/Users/stevens/pi-problems-30/runs30/$TAG
PROV="--provider $PROVIDER --model $MODEL"
NS="--no-session -na"
RESULTS=$ROOT/RESULTS.txt

# --- stage fresh copies of ALL problem scaffolding + seeds (never prior artifacts) ---
if [ "${PI30_RESUME:-0}" != "1" ]; then rm -rf "$ROOT"; fi; mkdir -p "$ROOT"
VERIF_FILES="verify.py check.py bench.py test_thing.py score.py converge_check.py PLAN.md"
SEED_FILES="roman.py fast.py kernel.py reduce.py integrator.py parens.py baseconv.py \
miniparse.py graph.py wordcount.py counter.py stats.py ttlcache.py intervals.py \
topo.py primecount.py limiter.py nsqrt.py det.py calc.py"
for n in $(seq 1 30); do
  p="p$n"; mkdir -p "$ROOT/$p"
  for f in $VERIF_FILES $SEED_FILES; do
    [ -f "$SRC/$p/$f" ] && cp "$SRC/$p/$f" "$ROOT/$p/$f"
  done
done
if [ "${PI30_RESUME:-0}" != "1" ]; then : > "$RESULTS"; fi
# >>> PI30_RESUME_PATCH v1 >>>
# Resume support. PI30_RESUME=1 keeps prior runs30/<tag>/RESULTS.txt and skips any
# problem already recorded PASS there (verdict lines "PN: PASS..."). Default (unset)
# = fresh full run (prior behavior). A problem that previously FAILED is re-run.
PI30_RESUME="${PI30_RESUME:-0}"
declare -A PI30_DONE=()
PRIOR_RESULTS="$ROOT/RESULTS.txt.prior"
if [ "$PI30_RESUME" = "1" ] && [ -f "$ROOT/RESULTS.txt" ]; then
  cp "$ROOT/RESULTS.txt" "$PRIOR_RESULTS"
  while IFS= read -r line; do
    pn=$(printf '%s' "$line" | sed -nE 's/^(P[0-9]+): PASS.*/\1/p')
    [ -n "$pn" ] && PI30_DONE[$pn]="$line"
  done < "$PRIOR_RESULTS"
  echo "[resume] carrying ${#PI30_DONE[@]} prior PASS problems: ${!PI30_DONE[*]}" >&2
fi
# skip_gate PN : if resuming and PN already PASSed, re-emit its cached line and return 0 (skip).
CUR_P=""
skip_gate() {
  CUR_P="$1"
  if [ "$PI30_RESUME" = "1" ] && [ -n "${PI30_DONE[$1]:-}" ]; then
    echo "${PI30_DONE[$1]}  [resumed-skip]" | tee -a "$RESULTS"
    return 0   # 0 = skip this problem
  fi
  return 1     # 1 = run this problem
}
# >>> PI30_RESUME_PATCH end >>>


# --- path-robustness fix (2026-07-04) ------------------------------------------
# Weaker tool-calling models (glm-4.7-flash, nemotron) INTERMITTENTLY emit a
# write-tool path that embeds the cwd (e.g. "private/tmp/<dir>/cli.py"), which pi
# joins onto cwd -> the artifact nests one level deep and the verifier (which
# checks $ROOT/pN/<file>) never finds it -> false FAIL. Across 30 problems one bad
# path tanks the whole lane to ~0. The ollama servers + native tool_calls are
# healthy (probed 2026-07-04); this is purely a path-location mismatch.
# Two layers, TOOLS STAY ON (no --no-tools): (1) system-prompt clamp telling the
# model to use bare relative filenames; (2) post-call flatten that lifts any
# nested artifacts back up into the problem dir before the verifier runs. Layer 2
# is the mesh-10 robustness property (harness controls artifact location) without
# abandoning tool use.
PATH_CLAMP="CRITICAL FILE-PATH RULE: when using the write or edit tools, ALWAYS pass a bare relative filename such as 'cli.py' or 'src/foo.py'. NEVER pass an absolute path. NEVER include /tmp, /Users, /private, or any part of the working directory in the path. The tool already runs in the correct directory. Writing to an absolute or cwd-prefixed path places the file in the wrong location and your work is lost."

# Lift artifacts the model nested under a cwd-echoed subpath back up to $dir.
# Only moves *.py files that DON'T already exist at top level (never clobbers a
# real seed/verifier file), and only from within $dir's own subtree.
flatten_nested() {
  local dir="$1"
  # find nested .py files (depth >= 2) not already present at top level
  find "$dir" -mindepth 2 -name '*.py' -type f 2>/dev/null | while read -r f; do
    # FIX (2026-07-05): NEVER flatten work/ subtrees. Fan-out problems
    # (P7/P17/P25) legitimately place sub-modules at work/<name>/<mod>.py and the
    # dispatcher/codec/pipeline imports them from there. The original flatten
    # lifted those up to the problem root, destroying the module the verifier
    # needs -> FALSE FAIL for EVERY model (not model-specific). Only flatten the
    # cwd-echoed nests (private/tmp/..., Users/...) the helper was built for.
    case "$f" in
      "$dir"/work/*) continue ;;
    esac
    local base; base="$(basename "$f")"
    if [ ! -e "$dir/$base" ]; then
      mv "$f" "$dir/$base" 2>/dev/null
    fi
  done
}

run_pi() { ( cd "$1" && $PT -p $PROV $NS --append-system-prompt "$PATH_CLAMP" "$2" ) >/dev/null 2>&1; flatten_nested "$1"; }
record() { echo "$1" | tee -a "$RESULTS"; }

echo "==== $TAG ($MODEL) START $(date) ====" | tee -a "$RESULTS"

# ============================ P1-P10 (tool-use) ============================
if ! skip_gate "P1"; then
record "[P1] stats CLI"
run_pi "$ROOT/p1" "Write cli.py: reads whitespace/newline-separated numbers from STDIN, prints exactly one line 'count=N min=.. max=.. mean=.. median=.. stdev=..' (stdev = SAMPLE stdev, n-1). median of even count = avg of two middle. Stdlib only. Exit 0."
(cd "$ROOT/p1" && "$PY" verify.py) >/dev/null 2>&1 && record "P1: PASS" || record "P1: FAIL"

fi  # end skip_gate block
if ! skip_gate "P2"; then
record "[P2] LRU cache + bundled tests"
run_pi "$ROOT/p2" "Implement lru.py with class LRUCache(capacity): get(key)->value-or-None, put(key,value), O(1), correct LRU eviction (get and put both count as use; put on existing key updates value AND refreshes recency). ALSO write test_lru.py with pytest tests and RUN pytest before done. Stdlib only."
(cd "$ROOT/p2" && "$PY" verify.py) >/dev/null 2>&1 && record "P2: PASS" || record "P2: FAIL"

fi  # end skip_gate block
if ! skip_gate "P3"; then
record "[P3] Roman numerals iterate-until-green"
for i in $(seq 1 8); do
  (cd "$ROOT/p3" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P3: PASS green in $i"; break; }
  F=$(cd "$ROOT/p3" && "$PYTEST" -q test_thing.py 2>&1 | tail -n 25)
  run_pi "$ROOT/p3" "pytest test_thing.py failing. Fix roman.py to use subtractive notation (IV IX XL XC CD CM). Smallest fix. DO NOT edit test_thing.py. Failures:
$F"
  [ "$i" = 8 ] && record "P3: FAIL after 8"
done

fi  # end skip_gate block
if ! skip_gate "P4"; then
record "[P4] stable softmax vs oracle"
for i in $(seq 1 6); do
  (cd "$ROOT/p4" && "$PY" check.py) >/dev/null 2>&1 && { record "P4: PASS in $i"; break; }
  O=$(cd "$ROOT/p4" && "$PY" check.py 2>&1 | tail -n 5)
  run_pi "$ROOT/p4" "fast.py softmax overflows / disagrees with reference in check.py. Fix for numerical stability (subtract max before exp). DO NOT edit check.py. Diagnostic:
$O"
  [ "$i" = 6 ] && record "P4: FAIL after 6"
done

fi  # end skip_gate block
if ! skip_gate "P5"; then
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

fi  # end skip_gate block
if ! skip_gate "P6"; then
record "[P6] reproducible FP reduction"
P6=0
for i in $(seq 1 5); do
  run_pi "$ROOT/p6" "Improve reduce.py parallel_sum(xs,nchunks) so result is BIT-IDENTICAL regardless of nchunks. Address CRITIQUE.md if present. Hint: math.fsum over all data or a fixed ordering independent of nchunks. DO NOT edit verify.py."
  run_pi "$ROOT/p6" "HOSTILE reviewer fresh eyes: inspect reduce.py ONLY for dependence of result on nchunks / non-deterministic FP ordering. Write findings to CRITIQUE.md. If zero real issues write exactly NO_ISSUES on first line."
  if head -n1 "$ROOT/p6/CRITIQUE.md" 2>/dev/null | grep -q NO_ISSUES && (cd "$ROOT/p6" && "$PY" verify.py) >/dev/null 2>&1; then
    record "P6: PASS critic+verifier in $i"; P6=1; break; fi
done
[ "$P6" = 0 ] && { (cd "$ROOT/p6" && "$PY" verify.py) >/dev/null 2>&1 && record "P6: PASS verifier (critic not satisfied)" || record "P6: FAIL"; }

fi  # end skip_gate block
if ! skip_gate "P7"; then
record "[P7] parallel backends fan-out"
mkdir -p "$ROOT/p7/work"
for be in csv kv json; do
  ( mkdir -p "$ROOT/p7/work/$be" && cd "$ROOT/p7/work/$be" && \
    $PT -p $PROV $NS "Per ../../PLAN.md implement ONLY the '$be' backend in backend.py exposing parse(text)->dict. csv:'a,b,c'->{'fields':[...]}. kv:'k1=v1;k2=v2'->{'k1':'v1',...}. json: JSON object string -> dict via stdlib json. Stdlib only." ) >/dev/null 2>&1 &
done
wait
run_pi "$ROOT/p7" "Backends exist at work/{csv,kv,json}/backend.py each exposing parse(text)->dict. Write dispatch.py exposing dispatch(kind,text)->dict routing kind in {csv,kv,json}. Run verify.py. DO NOT edit verify.py."
(cd "$ROOT/p7" && "$PY" verify.py) >/dev/null 2>&1 && record "P7: PASS" || record "P7: FAIL"

fi  # end skip_gate block
if ! skip_gate "P8"; then
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

fi  # end skip_gate block
if ! skip_gate "P9"; then
record "[P9] levenshtein tournament best-of-4"
mkdir -p "$ROOT/p9/arena"
for k in 1 2 3 4; do
  ( mkdir -p "$ROOT/p9/arena/cand_$k" && cd "$ROOT/p9/arena/cand_$k" && \
    $PT -p $PROV $NS "Write levenshtein.py exposing levenshtein(a,b)->int edit distance. CORRECT for all inputs incl empty, as FAST as possible (two-row DP, early exit). Stdlib only. Candidate #$k distinct angle." ) >/dev/null 2>&1 &
done
wait
best=""; bestf=0
for d in "$ROOT"/p9/arena/cand_*; do
  [ -f "$d/levenshtein.py" ] || continue
  f=$(cd "$ROOT/p9" && $SC "$PY" score.py "$d/levenshtein.py" 2>/dev/null); [ -z "$f" ] && f=0
  record "P9: $(basename $d) score=${f}"
  awk "BEGIN{exit !($f > $bestf)}" && { bestf=$f; best=$d; }
done
[ -n "$best" ] && awk "BEGIN{exit !($bestf > 0)}" && record "P9: PASS champion=$(basename $best) @ ${bestf}" || record "P9: FAIL no correct candidate"

fi  # end skip_gate block
if ! skip_gate "P10"; then
record "[P10] prime sieve capstone"
mkdir -p "$ROOT/p10/arena"
for k in 1 2 3; do
  ( mkdir -p "$ROOT/p10/arena/cand_$k" && cd "$ROOT/p10/arena/cand_$k" && \
    $PT -p $PROV $NS "Write sieve.py exposing primes_up_to(n)->sorted primes<=n. Correct for n<2 (empty), edge cases, FAST at n=2,000,000 (bytearray, skip evens, slice assign). Stdlib only. Candidate #$k distinct angle." ) >/dev/null 2>&1 &
done
wait
best=""; bestf=0
for d in "$ROOT"/p10/arena/cand_*; do
  [ -f "$d/sieve.py" ] || continue
  ( cd "$d" && $PT -p $PROV $NS "HOSTILE reviewer fresh eyes: inspect sieve.py for off-by-one (n included?), n<2, even bugs, slice-length bugs. If real bug, FIX sieve.py. Write VERDICT.txt: CLEAN or FIXED." ) >/dev/null 2>&1
  f=$(cd "$ROOT/p10" && $SC "$PY" score.py "$d/sieve.py" 2>/dev/null); [ -z "$f" ] && f=0
  record "P10: $(basename $d) verdict=$(head -1 "$d/VERDICT.txt" 2>/dev/null) score=${f}"
  awk "BEGIN{exit !($f > $bestf)}" && { bestf=$f; best=$d; }
done
[ -n "$best" ] && awk "BEGIN{exit !($bestf > 0)}" && record "P10: PASS champion=$(basename $best) @ ${bestf}" || record "P10: FAIL no correct candidate"

# ============================ P11-P30 (tool-use) ============================

fi  # end skip_gate block
if ! skip_gate "P11"; then
record "[P11] balanced parens iterate-until-green"
for i in $(seq 1 5); do
  (cd "$ROOT/p11" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P11: PASS green in $i"; break; }
  F=$(cd "$ROOT/p11" && "$PYTEST" -q test_thing.py 2>&1 | tail -15)
  run_pi "$ROOT/p11" "Fix parens.py: is_balanced(s)->bool validates (), [], {} matching via a stack, ignoring other chars. DO NOT edit test_thing.py. pytest failures:
$F"
  [ "$i" = 5 ] && record "P11: FAIL after 5"
done

fi  # end skip_gate block
if ! skip_gate "P12"; then
record "[P12] base-N conversion oracle"
for i in $(seq 1 5); do
  (cd "$ROOT/p12" && "$PY" check.py) >/dev/null 2>&1 && { record "P12: PASS in $i"; break; }
  O=$(cd "$ROOT/p12" && "$PY" check.py 2>&1 | tail -5)
  run_pi "$ROOT/p12" "Fix baseconv.py: to_base(n,base)->lowercase string and parse_int(s,base)->int for base 2..36, round-tripping and matching int(s,base). Handle 0 and negatives. DO NOT edit check.py. Diagnostic:
$O"
  [ "$i" = 5 ] && record "P12: FAIL after 5"
done

fi  # end skip_gate block
if ! skip_gate "P13"; then
record "[P13] mini-JSON parser iterate-until-green"
for i in $(seq 1 6); do
  (cd "$ROOT/p13" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P13: PASS green in $i"; break; }
  F=$(cd "$ROOT/p13" && "$PYTEST" -q test_thing.py 2>&1 | tail -18)
  run_pi "$ROOT/p13" "Fix miniparse.py: parse(s) parses a JSON subset (null/true/false/int/float/string/array/object, nesting, whitespace) WITHOUT using the json module or eval. DO NOT edit test_thing.py. pytest failures:
$F"
  [ "$i" = 6 ] && record "P13: FAIL after 6"
done

fi  # end skip_gate block
if ! skip_gate "P14"; then
record "[P14] weighted Dijkstra vs BFS-ref oracle"
for i in $(seq 1 5); do
  (cd "$ROOT/p14" && "$PY" check.py) >/dev/null 2>&1 && { record "P14: PASS in $i"; break; }
  O=$(cd "$ROOT/p14" && "$PY" check.py 2>&1 | tail -6)
  run_pi "$ROOT/p14" "Fix graph.py: shortest_path(graph,src,dst)->total weight of the min-cost path (graph is dict node->list[(neighbor,weight)], non-negative weights). Use Dijkstra (heapq). Return None/inf if unreachable per check.py's expectation. DO NOT edit check.py. Diagnostic:
$O"
  [ "$i" = 5 ] && record "P14: FAIL after 5"
done

fi  # end skip_gate block
if ! skip_gate "P15"; then
record "[P15] word-frequency top-k measurement (Mtok/s)"
best=0; stale=0; TARGET=1.0
for i in $(seq 1 6); do
  if ! (cd "$ROOT/p15" && "$PY" check.py) >/dev/null 2>&1; then
    O=$(cd "$ROOT/p15" && "$PY" check.py 2>&1 | tail -4)
    run_pi "$ROOT/p15" "Fix wordcount.py correctness: top_k(text,k)->list of (word,count) top-k by count then word, lowercased, split on whitespace. DO NOT edit check.py/bench.py. $O"; continue
  fi
  g=$(cd "$ROOT/p15" && "$PY" bench.py --report 2>/dev/null); [ -z "$g" ] && g=0
  record "P15: round $i -> ${g} Mtok/s"
  awk "BEGIN{exit !($g >= $TARGET)}" && { record "P15: PASS ${g} Mtok/s"; break; }
  awk "BEGIN{exit !($g > $best)}" && { best=$g; stale=0; } || stale=$((stale+1))
  [ $stale -ge 2 ] && { record "P15: STOP plateau best=${best}"; break; }
  run_pi "$ROOT/p15" "wordcount.top_k does ${g} Mtok/s. Make ONE change to go faster (collections.Counter / heapq.nlargest). Stay correct vs check.py. DO NOT edit check.py/bench.py."
  [ "$i" = 6 ] && record "P15: STOP budget best=${best}"
done

fi  # end skip_gate block
if ! skip_gate "P16"; then
record "[P16] thread-safe counter generator+critic"
P16=0
for i in $(seq 1 5); do
  run_pi "$ROOT/p16" "Fix counter.py so class Counter with increment() is thread-safe under concurrent threads (use threading.Lock around the shared count). Address CRITIQUE.md if present. DO NOT edit verify.py."
  run_pi "$ROOT/p16" "HOSTILE reviewer fresh eyes: inspect counter.py ONLY for data races / missing lock on the shared counter. Write findings to CRITIQUE.md. If zero real issues write exactly NO_ISSUES on first line."
  if head -n1 "$ROOT/p16/CRITIQUE.md" 2>/dev/null | grep -q NO_ISSUES && (cd "$ROOT/p16" && "$PY" verify.py) >/dev/null 2>&1; then
    record "P16: PASS critic+verifier in $i"; P16=1; break; fi
done
[ "$P16" = 0 ] && { (cd "$ROOT/p16" && "$PY" verify.py) >/dev/null 2>&1 && record "P16: PASS verifier (critic not satisfied)" || record "P16: FAIL"; }

fi  # end skip_gate block
if ! skip_gate "P17"; then
record "[P17] serializer fan-out (csv/kv/pylit + codec)"
for fmt in csv kv pylit; do
  ( mkdir -p "$ROOT/p17/work/$fmt" && cd "$ROOT/p17/work/$fmt" && \
    $PT -p $PROV $NS "Per ../../PLAN.md implement ONLY the '$fmt' backend in backend.py exposing dumps(obj)->str and loads(s)->obj. csv: obj {'fields':[...]} <-> 'a,b,c'. kv: flat {str:str} <-> 'k1=v1;k2=v2'. pylit: any literal, dumps=repr(obj), loads=ast.literal_eval(s) (stdlib ast only, never eval). Stdlib only." ) >/dev/null 2>&1 &
done
wait
run_pi "$ROOT/p17" "Backends exist at work/{csv,kv,pylit}/backend.py each exposing dumps(obj)->str and loads(s)->obj. Write codec.py exposing round_trip(fmt,obj)->loads(dumps(obj)) using the matching backend (import from work/<fmt>/backend.py). Run verify.py. DO NOT edit verify.py."
(cd "$ROOT/p17" && "$PY" verify.py) >/dev/null 2>&1 && record "P17: PASS" || record "P17: FAIL"

fi  # end skip_gate block
if ! skip_gate "P18"; then
record "[P18] Welford online variance reflection"
MB18=$(wc -c < /Users/stevens/.pi/agent/memory.md 2>/dev/null || echo 0)
for i in $(seq 1 5); do
  (cd "$ROOT/p18" && "$PY" converge_check.py) >/dev/null 2>&1 && { record "P18: PASS in $i"; break; }
  O=$(cd "$ROOT/p18" && "$PY" converge_check.py 2>&1 | tail -6)
  run_pi "$ROOT/p18" "Fix stats.py: running_variance(data)->SAMPLE variance (n-1) using Welford's online algorithm (numerically stable, no catastrophic cancellation, constant streams -> 0). Append a one-line LESSON to ~/.pi/agent/memory.md. DO NOT edit converge_check.py. $O"
  [ "$i" = 5 ] && record "P18: FAIL after 5"
done

fi  # end skip_gate block
if ! skip_gate "P19"; then
record "[P19] fast-doubling Fibonacci tournament"
mkdir -p "$ROOT/p19/arena"
for k in 1 2 3 4; do
  ( mkdir -p "$ROOT/p19/arena/cand_$k" && cd "$ROOT/p19/arena/cand_$k" && \
    $PT -p $PROV $NS "Write fib.py exposing fib(n)->the nth Fibonacci number (fib(0)=0,fib(1)=1), EXACT Python bigint, and FAST at n=200000 (use fast-doubling, O(log n)). Stdlib only. Candidate #$k distinct angle." ) >/dev/null 2>&1 &
done
wait
best=""; bestf=0
for d in "$ROOT"/p19/arena/cand_*; do
  [ -f "$d/fib.py" ] || continue
  f=$(cd "$ROOT/p19" && $SC "$PY" score.py "$d/fib.py" 2>/dev/null); [ -z "$f" ] && f=0
  record "P19: $(basename $d) score=${f}"
  awk "BEGIN{exit !($f > $bestf)}" && { bestf=$f; best=$d; }
done
[ -n "$best" ] && awk "BEGIN{exit !($bestf > 0)}" && record "P19: PASS champion=$(basename $best) @ ${bestf}" || record "P19: FAIL no correct candidate"

fi  # end skip_gate block
if ! skip_gate "P20"; then
record "[P20] TTL-LRU with injected clock iterate-until-green"
for i in $(seq 1 5); do
  (cd "$ROOT/p20" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P20: PASS green in $i"; break; }
  F=$(cd "$ROOT/p20" && "$PYTEST" -q test_thing.py 2>&1 | tail -18)
  run_pi "$ROOT/p20" "Fix ttlcache.py: class TTLCache(capacity, ttl, clock) — get/put honor LRU eviction AND TTL expiry using the injected clock() for time. Expired entries are misses. DO NOT edit test_thing.py. pytest failures:
$F"
  [ "$i" = 5 ] && record "P20: FAIL after 5"
done

fi  # end skip_gate block
if ! skip_gate "P21"; then
record "[P21] interval merge oracle"
for i in $(seq 1 5); do
  (cd "$ROOT/p21" && "$PY" check.py) >/dev/null 2>&1 && { record "P21: PASS in $i"; break; }
  O=$(cd "$ROOT/p21" && "$PY" check.py 2>&1 | tail -5)
  run_pi "$ROOT/p21" "Fix intervals.py: merge(intervals)->list of merged non-overlapping intervals, sorted, touching/overlapping intervals combined. DO NOT edit check.py. Diagnostic:
$O"
  [ "$i" = 5 ] && record "P21: FAIL after 5"
done

fi  # end skip_gate block
if ! skip_gate "P22"; then
record "[P22] toposort + cycle detect iterate-until-green"
for i in $(seq 1 5); do
  (cd "$ROOT/p22" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P22: PASS green in $i"; break; }
  F=$(cd "$ROOT/p22" && "$PYTEST" -q test_thing.py 2>&1 | tail -18)
  run_pi "$ROOT/p22" "Fix topo.py: toposort(graph)->a valid topological order (graph dict node->list[deps]); raise ValueError (or per test) on a cycle. DO NOT edit test_thing.py. pytest failures:
$F"
  [ "$i" = 5 ] && record "P22: FAIL after 5"
done

fi  # end skip_gate block
if ! skip_gate "P23"; then
record "[P23] prime-count sieve measurement (Mn/s)"
best=0; stale=0; TARGET=8.0
for i in $(seq 1 6); do
  if ! (cd "$ROOT/p23" && "$PY" check.py) >/dev/null 2>&1; then
    O=$(cd "$ROOT/p23" && "$PY" check.py 2>&1 | tail -3)
    run_pi "$ROOT/p23" "Fix primecount.py: count_primes(n)->number of primes below n, CORRECT for small n. DO NOT edit check.py/bench.py. $O"; continue
  fi
  g=$(cd "$ROOT/p23" && "$PY" bench.py --report 2>/dev/null); [ -z "$g" ] && g=0
  record "P23: round $i -> ${g} Mn/s"
  awk "BEGIN{exit !($g >= $TARGET)}" && { record "P23: PASS ${g} Mn/s"; break; }
  awk "BEGIN{exit !($g > $best)}" && { best=$g; stale=0; } || stale=$((stale+1))
  [ $stale -ge 2 ] && { record "P23: STOP plateau best=${best}"; break; }
  run_pi "$ROOT/p23" "primecount.count_primes does ${g} Mn/s. Make ONE change to go faster (Sieve of Eratosthenes with bytearray, skip evens). Stay correct vs check.py. DO NOT edit check.py/bench.py."
  [ "$i" = 6 ] && record "P23: STOP budget best=${best}"
done

fi  # end skip_gate block
if ! skip_gate "P24"; then
record "[P24] token-bucket rate limiter generator+critic"
P24=0
for i in $(seq 1 5); do
  run_pi "$ROOT/p24" "Fix limiter.py so class TokenBucket(rate, capacity, clock) allows at most 'capacity' burst then refills at 'rate' tokens/sec using the injected clock(); allow(n=1)->bool. Address CRITIQUE.md if present. DO NOT edit verify.py."
  run_pi "$ROOT/p24" "HOSTILE reviewer fresh eyes: inspect limiter.py ONLY for burst-exceeds-capacity / wrong refill math / clock misuse. Write findings to CRITIQUE.md. If zero real issues write exactly NO_ISSUES on first line."
  if head -n1 "$ROOT/p24/CRITIQUE.md" 2>/dev/null | grep -q NO_ISSUES && (cd "$ROOT/p24" && "$PY" verify.py) >/dev/null 2>&1; then
    record "P24: PASS critic+verifier in $i"; P24=1; break; fi
done
[ "$P24" = 0 ] && { (cd "$ROOT/p24" && "$PY" verify.py) >/dev/null 2>&1 && record "P24: PASS verifier (critic not satisfied)" || record "P24: FAIL"; }

fi  # end skip_gate block
if ! skip_gate "P25"; then
record "[P25] 3-stage stats pipeline fan-out"
for stage in clean agg fmt; do
  ( mkdir -p "$ROOT/p25/work/$stage" && cd "$ROOT/p25/work/$stage" && \
    $PT -p $PROV $NS "Per ../../PLAN.md implement ONLY the '$stage' stage in stage.py. clean: clean(rows)->list[float] dropping any element not convertible to float (None,'','x' dropped). agg: agg(nums)->{'count':int,'sum':float,'mean':float,'min':float,'max':float}. fmt: fmt(d)->single line 'k=v k=v ...' with keys ALPHA-sorted. Stdlib only." ) >/dev/null 2>&1 &
done
wait
run_pi "$ROOT/p25" "Stages exist at work/{clean,agg,fmt}/stage.py exposing clean/agg/fmt respectively. Write pipeline.py exposing run(rows)->fmt(agg(clean(rows))) (import each stage). Run verify.py. DO NOT edit verify.py."
(cd "$ROOT/p25" && "$PY" verify.py) >/dev/null 2>&1 && record "P25: PASS" || record "P25: FAIL"

fi  # end skip_gate block
if ! skip_gate "P26"; then
record "[P26] Newton sqrt to full precision reflection"
for i in $(seq 1 5); do
  (cd "$ROOT/p26" && "$PY" converge_check.py) >/dev/null 2>&1 && { record "P26: PASS in $i"; break; }
  O=$(cd "$ROOT/p26" && "$PY" converge_check.py 2>&1 | tail -6)
  run_pi "$ROOT/p26" "Fix nsqrt.py: nsqrt(x)->sqrt(x) to full double precision via Newton's method (iterate until convergence, handle 0 and 1, no math.sqrt). Append a one-line LESSON to ~/.pi/agent/memory.md. DO NOT edit converge_check.py. $O"
  [ "$i" = 5 ] && record "P26: FAIL after 5"
done

fi  # end skip_gate block
if ! skip_gate "P27"; then
record "[P27] overlapping substring count tournament"
mkdir -p "$ROOT/p27/arena"
for k in 1 2 3 4; do
  ( mkdir -p "$ROOT/p27/arena/cand_$k" && cd "$ROOT/p27/arena/cand_$k" && \
    $PT -p $PROV $NS "Write overlap.py exposing count_overlapping(haystack,needle)->int number of OVERLAPPING occurrences (count 'aa' in 'aaaa' == 3; str.count does NOT overlap so be cleverer). CORRECT incl empty needle -> 0, and FAST on long strings. Stdlib only. Candidate #$k distinct angle." ) >/dev/null 2>&1 &
done
wait
best=""; bestf=0
for d in "$ROOT"/p27/arena/cand_*; do
  [ -f "$d/overlap.py" ] || continue
  f=$(cd "$ROOT/p27" && $SC "$PY" score.py "$d/overlap.py" 2>/dev/null); [ -z "$f" ] && f=0
  record "P27: $(basename $d) score=${f}"
  awk "BEGIN{exit !($f > $bestf)}" && { bestf=$f; best=$d; }
done
[ -n "$best" ] && awk "BEGIN{exit !($bestf > 0)}" && record "P27: PASS champion=$(basename $best) @ ${bestf}" || record "P27: FAIL no correct candidate"

fi  # end skip_gate block
if ! skip_gate "P28"; then
record "[P28] matrix determinant vs numpy oracle"
for i in $(seq 1 5); do
  (cd "$ROOT/p28" && "$PY" check.py) >/dev/null 2>&1 && { record "P28: PASS in $i"; break; }
  O=$(cd "$ROOT/p28" && "$PY" check.py 2>&1 | tail -6)
  run_pi "$ROOT/p28" "Fix det.py: determinant(matrix)->float determinant of an NxN matrix (list of lists), matching numpy.linalg.det within tolerance for n>2 (LU / cofactor expansion). DO NOT edit check.py. Diagnostic:
$O"
  [ "$i" = 5 ] && record "P28: FAIL after 5"
done

fi  # end skip_gate block
if ! skip_gate "P29"; then
record "[P29] precedence calculator (no eval) iterate-until-green"
for i in $(seq 1 6); do
  (cd "$ROOT/p29" && "$PYTEST" -q test_thing.py) >/dev/null 2>&1 && { record "P29: PASS green in $i"; break; }
  F=$(cd "$ROOT/p29" && "$PYTEST" -q test_thing.py 2>&1 | tail -18)
  run_pi "$ROOT/p29" "Fix calc.py: calc(expr)->number, evaluating +-*/ with correct precedence and parentheses, WITHOUT using eval() (shunting-yard or recursive descent). DO NOT edit test_thing.py. pytest failures:
$F"
  [ "$i" = 6 ] && record "P29: FAIL after 6"
done

fi  # end skip_gate block
if ! skip_gate "P30"; then
record "[P30] sort-kernel capstone tournament + critic + bench"
mkdir -p "$ROOT/p30/arena"
for k in 1 2 3; do
  ( mkdir -p "$ROOT/p30/arena/cand_$k" && cd "$ROOT/p30/arena/cand_$k" && \
    $PT -p $PROV $NS "Write sort.py exposing my_sort(xs)->a new sorted list (ascending), CORRECT on all edge cases (empty, singletons, dupes, negatives, big ints) preserving multiset, and FAST on a large array. Stdlib only. Candidate #$k distinct angle." ) >/dev/null 2>&1 &
done
wait
best=""; bestf=0
for d in "$ROOT"/p30/arena/cand_*; do
  [ -f "$d/sort.py" ] || continue
  ( cd "$d" && $PT -p $PROV $NS "HOSTILE reviewer fresh eyes: inspect sort.py my_sort for stability of the multiset / edge cases (empty, negatives, dupes). If a real bug, FIX sort.py. Write VERDICT.txt: CLEAN or FIXED." ) >/dev/null 2>&1
  f=$(cd "$ROOT/p30" && $SC "$PY" score.py "$d/sort.py" 2>/dev/null); [ -z "$f" ] && f=0
  record "P30: $(basename $d) verdict=$(head -1 "$d/VERDICT.txt" 2>/dev/null) score=${f}"
  awk "BEGIN{exit !($f > $bestf)}" && { bestf=$f; best=$d; }
done
[ -n "$best" ] && awk "BEGIN{exit !($bestf > 0)}" && record "P30: PASS champion=$(basename $best) @ ${bestf}" || record "P30: FAIL no correct candidate"

fi  # end skip_gate block
echo "==== $TAG DONE $(date) ====" | tee -a "$RESULTS"
# SUMMARY to a SEPARATE file (avoid double-counting P-lines back into RESULTS)
{ echo "===== SUMMARY ($TAG / $MODEL) ====="
  grep -E "^P[0-9]+: (PASS|FAIL|STOP)" "$RESULTS"
  PASS=$(grep -cE "^P[0-9]+: PASS" "$RESULTS")
  echo "SCORE: $PASS/30 passed"
} > "$ROOT/SUMMARY.txt"
cat "$ROOT/SUMMARY.txt"
