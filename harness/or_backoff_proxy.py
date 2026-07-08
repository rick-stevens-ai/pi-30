#!/usr/bin/env python3
"""OpenRouter backoff/pacing proxy for pi-30 lanes.
Listens on localhost:8898, forwards /v1/* to OpenRouter, enforces a global
minimum inter-request spacing, and retries 429 (+5xx) with exponential backoff.
Key is read from ~/.pi/agent/models.json (openrouter-free provider).
"""
import json, os, time, threading
from flask import Flask, request, Response
import requests

CFG = os.path.expanduser("~/.pi/agent/models.json")
d = json.load(open(CFG))
KEY = d.get("providers", d)["openrouter-free"]["apiKey"]
UP = "https://openrouter.ai/api/v1"

MIN_GAP = float(os.environ.get("OR_MIN_GAP", "3.0"))
MAX_RETRY = int(os.environ.get("OR_MAX_RETRY", "8"))
BASE_BACKOFF = float(os.environ.get("OR_BASE_BACKOFF", "4.0"))
MAX_BACKOFF = float(os.environ.get("OR_MAX_BACKOFF", "90.0"))
REQ_TIMEOUT = float(os.environ.get("OR_REQ_TIMEOUT", "240"))

app = Flask(__name__)
_lock = threading.Lock()
_last = [0.0]
LOG = os.path.expanduser("~/pi-problems-30/or_backoff_proxy.log")


def log(m):
    line = time.strftime("%H:%M:%S") + " " + m
    with open(LOG, "a") as f:
        f.write(line + "\n")


def pace():
    with _lock:
        now = time.time()
        wait = MIN_GAP - (now - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()


@app.route("/v1/<path:p>", methods=["POST", "GET"])
def proxy(p):
    url = UP + "/" + p
    hdrs = {"Authorization": "Bearer " + KEY, "Content-Type": "application/json"}
    body = request.get_data()
    backoff = BASE_BACKOFF
    for attempt in range(1, MAX_RETRY + 1):
        pace()
        try:
            if request.method == "POST":
                r = requests.post(url, headers=hdrs, data=body, timeout=REQ_TIMEOUT)
            else:
                r = requests.get(url, headers=hdrs, timeout=REQ_TIMEOUT)
        except Exception as e:
            log("attempt %d EXC %s" % (attempt, e))
            time.sleep(min(backoff, MAX_BACKOFF))
            backoff *= 2
            continue
        if r.status_code == 429 or r.status_code in (502, 503, 504):
            ra = r.headers.get("Retry-After")
            wait = float(ra) if ra and ra.isdigit() else min(backoff, MAX_BACKOFF)
            log("attempt %d %d -> backoff %.1fs" % (attempt, r.status_code, wait))
            time.sleep(wait)
            backoff *= 2
            continue
        log("attempt %d %d OK" % (attempt, r.status_code))
        return Response(r.content, status=r.status_code,
                        content_type=r.headers.get("Content-Type", "application/json"))
    log("EXHAUSTED retries -> 429")
    return Response(json.dumps({"error": {"message": "proxy exhausted retries", "code": 429}}),
                    status=429, content_type="application/json")


if __name__ == "__main__":
    log("START min_gap=%s max_retry=%s base_backoff=%s" % (MIN_GAP, MAX_RETRY, BASE_BACKOFF))
    app.run(host="127.0.0.1", port=8898, threaded=True)
