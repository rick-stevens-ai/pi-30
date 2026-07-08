#!/bin/bash
# Rerun ONLY the failed fan-out problems (P7, P17, P25) against Laguna XS.2.
# Reuses run_model_30.sh's exact staging + helpers. Writes to a separate tag dir
# so the original 27/30 run is untouched.
set -u
unset PYTHONPATH
export CONDA_NO_PLUGINS=true
export PATH="/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
PI=/Users/stevens/.nvm/versions/node/v24.16.0/bin/pi
PY=/opt/anaconda3/bin/python3

GT=$(command -v gtimeout || command -v timeout)
PI_TIMEOUT="${PI_TIMEOUT:-300}"
PT="$GT -k 15 $PI_TIMEOUT $PI"
[ -z "$GT" ] && { echo "FATAL: no gtimeout/timeout"; exit 2; }

PROVIDER="laguna-uicgpu"; MODEL="laguna-xs2"; TAG="laguna-xs2-rerun"
SRC=/Users/stevens/pi-problems-30
ROOT=/Users/stevens/pi-problems-30/runs30/$TAG
PROV="--provider $PROVIDER --model $MODEL"
NS="--no-session -na"
RESULTS=$ROOT/RESULTS.txt

rm -rf "$ROOT"; mkdir -p "$ROOT"
VERIF_FILES="verify.py check.py bench.py test_thing.py score.py converge_check.py PLAN.md"
for n in 7 17 25; do
  p="p$n"; mkdir -p "$ROOT/$p"
  for f in $VERIF_FILES; do
    [ -f "$SRC/$p/$f" ] && cp "$SRC/$p/$f" "$ROOT/$p/$f"
  done
done
: > "$RESULTS"

PATH_CLAMP="CRITICAL FILE-PATH RULE: when using the write or edit tools, ALWAYS pass a bare relative filename such as 'cli.py' or 'src/foo.py'. NEVER pass an absolute path. NEVER include /tmp, /Users, /private, or any part of the working directory in the path. The tool already runs in the correct directory. Writing to an absolute or cwd-prefixed path places the file in the wrong location and your work is lost."

flatten_nested() {
  local dir="$1"
  # FIX (2026-07-05): exclude work/ subtrees. Fan-out problems (P7/P17/P25)
  # legitimately place sub-modules at work/<name>/backend.py and the dispatcher
  # imports them from there. The original flatten lifted those up to the problem
  # root, destroying the module the verifier needs -> false FAIL for EVERY model.
  # Only flatten cwd-echoed nests like private/tmp/... , never work/*.
  find "$dir" -mindepth 2 -name '*.py' -type f 2>/dev/null | while read -r f; do
    case "$f" in
      "$dir"/work/*) continue ;;
    esac
    local base; base="$(basename "$f")"
    if [ ! -e "$dir/$base" ]; then mv "$f" "$dir/$base" 2>/dev/null; fi
  done
}
run_pi() { ( cd "$1" && $PT -p $PROV $NS --append-system-prompt "$PATH_CLAMP" "$2" ) >/dev/null 2>&1; flatten_nested "$1"; }
record() { echo "$1" | tee -a "$RESULTS"; }

echo "==== $TAG ($MODEL) RERUN START $(date) ====" | tee -a "$RESULTS"

# ---------- P7 ----------
record "[P7] parallel backends fan-out"
mkdir -p "$ROOT/p7/work"
for be in csv kv json; do
  ( mkdir -p "$ROOT/p7/work/$be" && cd "$ROOT/p7/work/$be" && \
    $PT -p $PROV $NS "Per ../../PLAN.md implement ONLY the '$be' backend in backend.py exposing parse(text)->dict. csv:'a,b,c'->{'fields':[...]}. kv:'k1=v1;k2=v2'->{'k1':'v1',...}. json: JSON object string -> dict via stdlib json. Stdlib only." ) >/dev/null 2>&1 &
done
wait
run_pi "$ROOT/p7" "Backends exist at work/{csv,kv,json}/backend.py each exposing parse(text)->dict. Write dispatch.py exposing dispatch(kind,text)->dict routing kind in {csv,kv,json}. Run verify.py. DO NOT edit verify.py."
(cd "$ROOT/p7" && "$PY" verify.py) >/dev/null 2>&1 && record "P7: PASS" || record "P7: FAIL"

# ---------- P17 ----------
record "[P17] serializer fan-out (csv/kv/pylit + codec)"
for fmt in csv kv pylit; do
  ( mkdir -p "$ROOT/p17/work/$fmt" && cd "$ROOT/p17/work/$fmt" && \
    $PT -p $PROV $NS "Per ../../PLAN.md implement ONLY the '$fmt' backend in backend.py exposing dumps(obj)->str and loads(s)->obj. csv: obj {'fields':[...]} <-> 'a,b,c'. kv: flat {str:str} <-> 'k1=v1;k2=v2'. pylit: any literal, dumps=repr(obj), loads=ast.literal_eval(s) (stdlib ast only, never eval). Stdlib only." ) >/dev/null 2>&1 &
done
wait
run_pi "$ROOT/p17" "Backends exist at work/{csv,kv,pylit}/backend.py each exposing dumps(obj)->str and loads(s)->obj. Write codec.py exposing round_trip(fmt,obj)->loads(dumps(obj)) using the matching backend (import from work/<fmt>/backend.py). Run verify.py. DO NOT edit verify.py."
(cd "$ROOT/p17" && "$PY" verify.py) >/dev/null 2>&1 && record "P17: PASS" || record "P17: FAIL"

# ---------- P25 ----------
record "[P25] 3-stage stats pipeline fan-out"
for stage in clean agg fmt; do
  ( mkdir -p "$ROOT/p25/work/$stage" && cd "$ROOT/p25/work/$stage" && \
    $PT -p $PROV $NS "Per ../../PLAN.md implement ONLY the '$stage' stage in stage.py. clean: clean(rows)->list[float] dropping any element not convertible to float (None,'','x' dropped). agg: agg(nums)->{'count':int,'sum':float,'mean':float,'min':float,'max':float}. fmt: fmt(d)->single line 'k=v k=v ...' with keys ALPHA-sorted. Stdlib only." ) >/dev/null 2>&1 &
done
wait
run_pi "$ROOT/p25" "Stages exist at work/{clean,agg,fmt}/stage.py exposing clean/agg/fmt respectively. Write pipeline.py exposing run(rows)->fmt(agg(clean(rows))) (import each stage). Run verify.py. DO NOT edit verify.py."
(cd "$ROOT/p25" && "$PY" verify.py) >/dev/null 2>&1 && record "P25: PASS" || record "P25: FAIL"

echo "==== $TAG RERUN DONE $(date) ====" | tee -a "$RESULTS"
