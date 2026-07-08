# pi multi-model agent-loop sweep — engineering notes

Project: run the "Vibe Coding with the Pi Agent Loop" curriculum (30 verification-
gated problems) across ALL free models Rick hosts/can reach, compare pass-rates.

## TOOL-USE DIAGNOSIS (2026-06-29) — the core blocker and fixes

pi sends OpenAI tool schemas. Models reply with their NATIVE tool-call dialect
(qwen3-coder emits `<function=write><parameter=path>...`). The serving runtime
must have a PARSER that converts that dialect → structured `tool_calls`. If it
doesn't, pi sees raw text and writes no artifact.

### Per-runtime tool-calling status (verified)
- **Ollama 0.30.6 (spark-36ac, <tailnet-host>:11434)**: per-model. qwen3-coder:30b
  + devstral-small-2:24b advertise Tools and return structured tool_calls for a
  SIMPLE tool, BUT with pi's write/edit schema qwen3-coder emits raw XML text
  Ollama does NOT parse → no file. codestral:22b, phi4:14b = "does not support
  tools". VERDICT: Ollama UNRELIABLE for pi tool-use.
- **LM Studio (m3acbook <tailnet-host>:1234, macOS 26.3.1, 55 models)**: returns
  CORRECT structured tool_calls for qwen3-coder, JIT-loads on demand. WORKS for
  pi tool-use. lms CLI at "/Applications/LM Studio.app/Contents/Resources/app/.webpack/lms".
  Models incl AuroraGPT variants, qwen3-coder-30b, gpt-oss-120b/20b, glm-4.7-flash,
  deepseek-r1-distill-llama-70b, qwen3-next-80b, seed-oss-36b, gemma-3-27b.
- **studio-ts (studio host)**: reachable; lms not found yet — LM Studio may not be
  installed/serving there. Need to confirm.
- **vLLM**: the proper fix for Sparks. `--enable-auto-tool-choice --tool-call-parser P`
  where P = qwen3_xml (qwen3-coder), hermes (qwen3 general), llama3_json (llama3.3),
  mistral (devstral/mistral), openai (gpt-oss), glm47 (glm-4.x), + matching
  --chat-template from vllm examples/. NOT installed on spark-36ac (Ollama only;
  docker has open-webui + comfyui).

### Universal fallback that works on ALL models
Code-extraction harness: pi --no-tools, ask for ONE fenced code block, extract +
write the artifact ourselves, verdict from verifier exit code.
  - run_model_extract.sh + extract_code.py (10-problem subset)
  - Confirmed: spark qwen3-coder:30b scores P1/P2/P3 PASS via extraction (tool-use=0).

## THREE ENABLEMENT PATHS (Rick approved "go for it", 2026-06-29)
1. LM Studio (m3acbook + studio-ts) — works now, register as pi provider, tool-use harness.
2. vLLM on Sparks — install + serve per-model with right --tool-call-parser. Proper Spark fix.
3. Code-extraction — universal baseline, every model incl no-tool ones.

## pi providers registered (~/.pi/agent/models.json)
- spark36       → http://<tailnet-host>:11434/v1 (Ollama, no auth)
- ollama-cloud  → https://ollama.com/v1 (key from ~/Dropbox/AIEN/keys-misc.md rotated line)
- openrouter-free → https://openrouter.ai/api/v1 (key from AIEN env.sh; free tier 429-throttled)
- lmstudio-m3   → http://<tailnet-host>:1234/v1 (LM Studio, no auth, JIT load)

## Model universe (~80 free, heavy overlap)
- Sparks spark-36ac Ollama: 24 (Rick priority). spark-95fe/9611 = Qwen3-235B TP=2, DO NOT TOUCH.
- LM Studio m3acbook: 55. Ollama Cloud Pro: 35. OpenRouter free: ~24. CELS: 5. Sophia: 9 (Ollie).

## Curriculum
30 problems p1..p30 under ~/pi-kimi-loops/. Each = verifier (never edited) + seed
(broken, or correct-but-slow for measurement loops p5/p15/p23). All seeds pre-
confirmed failing. Verifiers run via /opt/anaconda3/bin/python3 (numpy+numba+pytest).
Method ladder L1-L10 (single-shot, bundled-tests, iterate-until-green, oracle,
measurement, generator+critic, fan-out, reflection, tournament, capstone) x3.

## Verdict discipline
Verdicts come from verifier EXIT CODES, never the model's prose. Seeds must fail
before looping (loop must earn the fix).

## LM Studio (m3acbook <tailnet-host>:1234) — bind fix
ROOT CAUSE of all earlier "Connection error" / HTTP=000-in-13ms from pi:
LM Studio server was bound to 127.0.0.1 only (localhost). `lms ps`/`lms load`
work because they run locally on m3acbook, but ANY request from m1 over
Tailscale to 127.0.0.1 gets instant connection reset. NOT JIT latency.

FIX: restart with network bind:
  lms server stop; lms server start --bind 0.0.0.0
Confirm: lsof -nP -iTCP:1234 -sTCP:LISTEN  -> should show *:1234 (not 127.0.0.1)
Reload model after restart (server restart unloads): lms load <model> --ttl 3600
Verified: curl from m1 -> HTTP=200 PONG in 4.9s. tool_calls field present (empty when none).
CONTEXT WINDOW = 4096 only — may truncate full pi agentic turns; bump per-model if needed.
Persist: set LMS_SERVER_HOST=0.0.0.0 or always pass --bind 0.0.0.0 on start.
