#!/usr/bin/env python3
"""Official Codex adapter for the pi-30 course benchmark (Lab 1, CMSC 35200).

Drives the Codex CLI across the 30 problems and emits the canonical runs.csv
(one row per attempt). Verifier exit code is the sole authority.

Codex protocol note: current Codex (>=0.158) requires wire_api="responses".
The provider (model_provider "dls_qwen") must already be configured at
~/.codex/config.toml with base_url=<chicago-6>/v1 and wire_api="responses"
(set up in Part A). This adapter never takes an API key on the command line.

Usage:
  python3 adapters/codex_adapter.py \
     --model qwen3.8-27b --endpoint-label chicago-6 \
     --problems ./problems --runs ./runs_lab1 --csv ./runs.csv \
     [--tasks P1,P2] [--codex /path/to/codex] [--timeout 400]
"""
import argparse, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common  # noqa
from runs_schema import FIELDS  # noqa

TOKENS_RE = re.compile(r"tokens used[:\s]*([\d,]+)", re.I)


def codex_version(codex_bin):
    try:
        return subprocess.check_output([codex_bin, "--version"], text=True).strip().splitlines()[0]
    except Exception:
        return "unknown"


def make_codex_runner(codex_bin, timeout):
    def run_once(workdir, prompt, attempt_idx):
        logdir = os.path.join(workdir, "_logs")
        os.makedirs(logdir, exist_ok=True)
        out_p = os.path.join(logdir, f"attempt{attempt_idx}.stdout")
        err_p = os.path.join(logdir, f"attempt{attempt_idx}.stderr")
        last_p = os.path.join(logdir, f"attempt{attempt_idx}.last")
        # Bounded authority: workspace-write sandbox, approvals never (non-interactive),
        # web search on. No --dangerously-* flags.
        cmd = [codex_bin, "exec", "--skip-git-repo-check",
               "--sandbox", "workspace-write",
               "-c", "approval_policy=never",
               "--search",
               "-o", last_p, prompt]
        infra = False
        stdout_text = ""
        try:
            with open(out_p, "w") as o, open(err_p, "w") as e:
                r = subprocess.run(cmd, cwd=workdir, stdout=o, stderr=e,
                                   timeout=timeout, check=False)
            stdout_text = _read(out_p)
            # A streaming/transport failure shows up as "Reconnecting" / "high demand".
            if "exceeded retry limit" in stdout_text or "We're currently experiencing high demand" in stdout_text:
                infra = True
        except subprocess.TimeoutExpired:
            infra = True
        except Exception:
            infra = True
        # Parse token telemetry from Codex output ("tokens used: N").
        total = "unknown"
        m = TOKENS_RE.search(stdout_text)
        if m:
            try:
                total = int(m.group(1).replace(",", ""))
            except Exception:
                total = "unknown"
        # count tool-call markers Codex prints (exec/apply_patch), best-effort
        tool_calls = "unknown"
        tc = len(re.findall(r"^\s*(exec|apply_patch|command)\b", stdout_text, re.M))
        if tc:
            tool_calls = tc
        return {
            "text": stdout_text[-4000:], "infra_error": infra,
            "prompt_tokens": "unknown", "completion_tokens": "unknown",
            "reasoning_tokens": "unknown", "total_tokens": total,
            "tool_calls": tool_calls, "retry_count": "unknown",
            "stdout_path": os.path.relpath(out_p, workdir),
            "stderr_path": os.path.relpath(err_p, workdir),
            "transcript_path": os.path.relpath(out_p, workdir),
        }
    return run_once


def _read(path, n=20000):
    try:
        with open(path) as f:
            return f.read()[-n:]
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="qwen3.8-27b")
    ap.add_argument("--endpoint-label", default="chicago-6")
    ap.add_argument("--problems", default=os.path.join(common.REPO, "problems"))
    ap.add_argument("--runs", default=os.path.join(common.REPO, "runs_lab1"))
    ap.add_argument("--csv", default=os.path.join(common.REPO, "runs.csv"))
    ap.add_argument("--tasks", default="")
    ap.add_argument("--codex", default=os.environ.get("CODEX_BIN", "codex"))
    ap.add_argument("--timeout", type=int, default=400)
    ap.add_argument("--max-iters", type=int, default=0)
    a = ap.parse_args()

    tasks = [t.strip().upper() for t in a.tasks.split(",") if t.strip()] or \
            [f"P{i}" for i in range(1, 31)]
    ver = codex_version(a.codex)
    runner = make_codex_runner(a.codex, a.timeout)
    print(f"[codex_adapter] codex={ver} model={a.model} tasks={len(tasks)}")
    for t in tasks:
        st, vs, sc = common.run_task(
            "codex", t, runner, a.problems, a.runs, a.csv,
            a.model, a.endpoint_label, ver,
            max_iters_override=(a.max_iters or None))
        print(f"  {t}: status={st} verifier={vs} score={sc}")
    print(f"[codex_adapter] done -> {a.csv}")


if __name__ == "__main__":
    main()
