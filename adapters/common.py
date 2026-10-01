"""Shared runner for the pi-30 course adapters (Lab 1, CMSC 35200).

Responsibilities (identical for Pi and Codex so the comparison is controlled):
  * stage a FRESH workspace per task from problems/pN (verifier + seed files only;
    never prior run artifacts, never solution files);
  * drive the task's prompt(s) through an agent runner callback, honoring the
    task's iterate-until-green loop budget;
  * run the verifier/scorer and take its EXIT CODE as the sole source of truth;
  * flatten cwd-echoed nested artifacts back into the task dir (robustness);
  * append one runs.csv row per attempt with full telemetry (unknown where a
    runtime does not expose a field).

The agent runner callback signature:
    run_once(workdir, prompt, attempt_idx) -> dict with keys:
        text, prompt_tokens, completion_tokens, reasoning_tokens, total_tokens,
        tool_calls, retry_count, stdout_path, stderr_path, transcript_path
    Any unknown numeric field should be the string "unknown".
"""
from __future__ import annotations
import json, os, shutil, subprocess, sys, time, datetime, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SPEC = json.load(open(os.path.join(HERE, "tasks_spec.json")))

VERIF_FILES = ["verify.py", "check.py", "bench.py", "test_thing.py", "score.py",
               "converge_check.py", "PLAN.md", "CRITIQUE.md"]
SEED_FILES = ["roman.py", "fast.py", "kernel.py", "reduce.py", "integrator.py",
              "parens.py", "baseconv.py", "miniparse.py", "graph.py", "wordcount.py",
              "counter.py", "stats.py", "ttlcache.py", "intervals.py", "topo.py",
              "primecount.py", "limiter.py", "nsqrt.py", "det.py", "calc.py"]

PATH_CLAMP = ("CRITICAL FILE-PATH RULE: when writing or editing files, ALWAYS use a "
              "bare relative filename such as 'cli.py'. NEVER use an absolute path and "
              "never include /tmp, /Users, /private, or any part of the working "
              "directory. The tool already runs in the correct directory.")


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def harness_commit():
    try:
        return subprocess.check_output(["git", "-C", REPO, "rev-parse", "--short", "HEAD"],
                                       text=True).strip()
    except Exception:
        return "unknown"


def stage_workspace(task_id, dest, problems_dir):
    src = os.path.join(problems_dir, "p" + task_id[1:])
    os.makedirs(dest, exist_ok=True)
    for f in VERIF_FILES + SEED_FILES:
        s = os.path.join(src, f)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(dest, f))


def flatten_nested(dest):
    for f in glob.glob(os.path.join(dest, "**", "*.py"), recursive=True):
        rel = os.path.relpath(f, dest)
        if os.sep not in rel:
            continue
        if rel.startswith("work" + os.sep):   # legit fan-out submodules
            continue
        top = os.path.join(dest, os.path.basename(f))
        if not os.path.exists(top):
            shutil.move(f, top)


def _verifier_diag(task_id, dest, timeout=60):
    """Capture the verifier's stderr/stdout tail for retry feedback (iterate tasks)."""
    spec = SPEC[task_id]; v = spec["verify"]
    py = os.environ.get("PI30_PY", sys.executable)
    try:
        if v == "test_thing.py":
            r = subprocess.run([py, "-m", "pytest", "-q", "test_thing.py"],
                               cwd=dest, capture_output=True, timeout=timeout, text=True)
        elif v in ("bench.py",):
            r = subprocess.run([py, "check.py"], cwd=dest, capture_output=True, timeout=timeout, text=True)
        else:
            r = subprocess.run([py, v], cwd=dest, capture_output=True, timeout=timeout, text=True)
        return ((r.stdout or "") + "\n" + (r.stderr or "")).strip()
    except Exception as e:
        return f"(diagnostic capture failed: {e})"


def run_verifier(task_id, dest, timeout=120):
    """Return (verifier_status, score). verifier_status in pass|fail|error."""
    spec = SPEC[task_id]
    v = spec["verify"]
    py = os.environ.get("PI30_PY", sys.executable)
    score = "unknown"
    try:
        if v == "test_thing.py":
            r = subprocess.run([py, "-m", "pytest", "-q", "test_thing.py"],
                               cwd=dest, capture_output=True, timeout=timeout)
            return ("pass" if r.returncode == 0 else "fail", score)
        if v == "bench.py":
            # OPTIMIZE task: correctness (check.py) must pass AND the benchmark
            # throughput must meet the task's target. bench.py prints the metric but
            # does NOT gate on the target, so we enforce the target here (the values
            # match the reference harness run_model_30.sh).
            OPT_TARGETS = {"P5": 5.0, "P15": 1.0, "P23": 8.0}
            r = subprocess.run([py, "check.py"], cwd=dest, capture_output=True, timeout=timeout)
            if r.returncode != 0:
                return ("fail", score)
            b = subprocess.run([py, "bench.py", "--report"], cwd=dest,
                               capture_output=True, timeout=timeout, text=True)
            try:
                score = float((b.stdout or "0").strip().split()[0])
            except Exception:
                score = "unknown"
            target = OPT_TARGETS.get(task_id)
            if target is not None and isinstance(score, float):
                return ("pass" if score >= target else "fail", score)
            return ("fail" if score == "unknown" else "pass", score)
        if v == "score.py":
            r = subprocess.run([py, "score.py"], cwd=dest, capture_output=True, timeout=timeout, text=True)
            try:
                score = float((r.stdout or "0").strip().split()[0])
                passed = score > 0
            except Exception:
                passed = (r.returncode == 0)
            return ("pass" if passed else "fail", score)
        # verify.py / check.py / converge_check.py => exit-code authority
        r = subprocess.run([py, v], cwd=dest, capture_output=True, timeout=timeout)
        return ("pass" if r.returncode == 0 else "fail", score)
    except subprocess.TimeoutExpired:
        return ("error", score)
    except Exception:
        return ("error", score)


def map_status(verifier_status, agent_result):
    if agent_result.get("infra_error"):
        return "infra_error"
    if verifier_status == "pass":
        return "verified_success"
    if verifier_status == "error":
        return "task_failed"
    return "task_failed"


def run_task(agent_name, task_id, run_once, problems_dir, runs_root, csv_path,
             model, endpoint_label, agent_version, max_iters_override=None):
    """Drive one task end-to-end for one agent; append per-attempt rows."""
    from runs_schema import append_row
    spec = SPEC[task_id]
    dest = os.path.join(runs_root, agent_name, "p" + task_id[1:])
    shutil.rmtree(dest, ignore_errors=True)
    stage_workspace(task_id, dest, problems_dir)
    prompts = spec["prompts"] or [
        f"Solve task {task_id} ({spec['title']}). Inspect the files in this directory, "
        f"including the verifier, and make the verifier pass. Do not edit the verifier."]
    max_iters = max_iters_override or spec["max_iters"]
    hc = harness_commit()
    final_status, final_vstatus, final_score = "not_run", "not_run", "unknown"
    attempt = 0
    is_iterate = spec["kind"] in ("fix", "numerical", "optimize", "reflection")
    last_diag = ""
    for i in range(max_iters):
        prompt = prompts[min(i, len(prompts) - 1)]
        prompt = PATH_CLAMP + "\n\n" + prompt
        # On iterate-until-green tasks, feed the verifier's own failure output back
        # into each retry (mirrors the reference harness) so the agent can debug.
        if is_iterate and i > 0 and last_diag:
            prompt += ("\n\nThe verifier is still failing. Do NOT edit the verifier/"
                       "test files. Latest diagnostic output:\n" + last_diag[-2000:])
        attempt += 1
        t0 = time.time(); s0 = utc()
        res = run_once(dest, prompt, attempt)
        flatten_nested(dest)
        vstatus, score = run_verifier(task_id, dest)
        last_diag = _verifier_diag(task_id, dest) if vstatus != "pass" else ""
        t1 = time.time(); s1 = utc()
        status = map_status(vstatus, res)
        append_row(csv_path, {
            "agent": agent_name, "task_id": task_id, "attempt": attempt,
            "start_utc": s0, "end_utc": s1, "wall_seconds": round(t1 - t0, 3),
            "status": status, "verifier_status": vstatus, "score": score,
            "prompt_tokens": res.get("prompt_tokens", "unknown"),
            "completion_tokens": res.get("completion_tokens", "unknown"),
            "reasoning_tokens": res.get("reasoning_tokens", "unknown"),
            "total_tokens": res.get("total_tokens", "unknown"),
            "tool_calls": res.get("tool_calls", "unknown"),
            "retry_count": res.get("retry_count", "unknown"),
            "model": model, "endpoint_label": endpoint_label,
            "pi_or_codex_version": agent_version, "harness_commit": hc,
            "stdout_path": res.get("stdout_path", "unknown"),
            "stderr_path": res.get("stderr_path", "unknown"),
            "transcript_path": res.get("transcript_path", "unknown"),
        })
        final_status, final_vstatus, final_score = status, vstatus, score
        if vstatus == "pass":
            break
    return final_status, final_vstatus, final_score
