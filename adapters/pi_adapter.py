#!/usr/bin/env python3
"""Official Pi adapter for the pi-30 course benchmark (Lab 1, CMSC 35200).

Drives the Pi coding agent across the 30 problems and emits the canonical
runs.csv (one row per attempt). Verifier exit code is the sole authority.

Usage:
  python3 adapters/pi_adapter.py \
     --provider dls-qwen --model qwen3.8-27b \
     --endpoint-label chicago-6 \
     --problems ./problems --runs ./runs_lab1 --csv ./runs.csv \
     [--tasks P1,P2,P3] [--pi /path/to/pi] [--timeout 300]

Credentials come from the Pi provider config (set up in Part A); this adapter
never takes an API key on the command line.
"""
import argparse, json, os, re, subprocess, sys, time, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common  # noqa
from runs_schema import FIELDS  # noqa


def pi_version(pi_bin):
    try:
        return subprocess.check_output([pi_bin, "--version"], text=True).strip().splitlines()[0]
    except Exception:
        return "unknown"


def make_pi_runner(pi_bin, provider, model, timeout):
    def run_once(workdir, prompt, attempt_idx):
        logdir = os.path.join(workdir, "_logs")
        os.makedirs(logdir, exist_ok=True)
        out_p = os.path.join(logdir, f"attempt{attempt_idx}.stdout")
        err_p = os.path.join(logdir, f"attempt{attempt_idx}.stderr")
        cmd = [pi_bin, "--provider", provider, "--model", model,
               "--no-session", "-na", "--print", prompt]
        infra = False
        try:
            with open(out_p, "w") as o, open(err_p, "w") as e:
                subprocess.run(cmd, cwd=workdir, stdout=o, stderr=e,
                               timeout=timeout, check=False)
        except subprocess.TimeoutExpired:
            infra = True
        except Exception:
            infra = True
        # Pi CLI does not emit structured token telemetry in --print mode.
        return {
            "text": _tail(out_p), "infra_error": infra,
            "prompt_tokens": "unknown", "completion_tokens": "unknown",
            "reasoning_tokens": "unknown", "total_tokens": "unknown",
            "tool_calls": "unknown", "retry_count": "unknown",
            "stdout_path": os.path.relpath(out_p, workdir),
            "stderr_path": os.path.relpath(err_p, workdir),
            "transcript_path": os.path.relpath(out_p, workdir),
        }
    return run_once


def _tail(path, n=4000):
    try:
        with open(path) as f:
            return f.read()[-n:]
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="dls-qwen")
    ap.add_argument("--model", default="qwen3.8-27b")
    ap.add_argument("--endpoint-label", default="chicago-6")
    ap.add_argument("--problems", default=os.path.join(common.REPO, "problems"))
    ap.add_argument("--runs", default=os.path.join(common.REPO, "runs_lab1"))
    ap.add_argument("--csv", default=os.path.join(common.REPO, "runs.csv"))
    ap.add_argument("--tasks", default="")
    ap.add_argument("--pi", default=os.environ.get("PI_BIN", "pi"))
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--max-iters", type=int, default=0)
    a = ap.parse_args()

    tasks = [t.strip().upper() for t in a.tasks.split(",") if t.strip()] or \
            [f"P{i}" for i in range(1, 31)]
    ver = pi_version(a.pi)
    runner = make_pi_runner(a.pi, a.provider, a.model, a.timeout)
    print(f"[pi_adapter] pi={ver} provider={a.provider} model={a.model} tasks={len(tasks)}")
    for t in tasks:
        st, vs, sc = common.run_task(
            "pi", t, runner, a.problems, a.runs, a.csv,
            a.model, a.endpoint_label, ver,
            max_iters_override=(a.max_iters or None))
        print(f"  {t}: status={st} verifier={vs} score={sc}")
    print(f"[pi_adapter] done -> {a.csv}")


if __name__ == "__main__":
    main()
