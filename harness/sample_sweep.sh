#!/bin/bash
# Sample sweep: ~3 models per source through the code-extraction harness (10 probs).
# Spark first (Rick's priority). Sequential to avoid GB10 contention + keep logs clean.
cd /Users/stevens/pi-problems-30
S=bash\ run_model_extract.sh

run() { echo ">>>> $(date) START $3"; bash run_model_extract.sh "$1" "$2" "$3" --no-tools; echo ">>>> $(date) END $3"; }

# --- SPARKS (priority): top coder / mid / small ---
run spark36 "qwen3-coder:30b"        spark-qwen3coder30b
run spark36 "gpt-oss:20b"            spark-gptoss20b
run spark36 "qwen3:14b"              spark-qwen3-14b

# --- OLLAMA CLOUD: big coder / frontier general / mid ---
run ollama-cloud "qwen3-coder:480b"  oc-qwen3coder480b
run ollama-cloud "glm-5.1"           oc-glm51
run ollama-cloud "gemma4:31b"        oc-gemma4-31b

# --- OPENROUTER FREE: coder / nemotron / llama (expect some 429s) ---
run openrouter-free "openai/gpt-oss-120b:free"                   or-gptoss120b
run openrouter-free "nvidia/nemotron-3-super-120b-a12b:free"     or-nemotron-super
run openrouter-free "meta-llama/llama-3.3-70b-instruct:free"     or-llama33-70b

echo "==== SAMPLE SWEEP COMPLETE $(date) ===="
echo "===== SCORES ====="
for d in /Users/stevens/pi-problems-30/runs_extract/*/RESULTS.txt; do
  t=$(basename $(dirname "$d"))
  s=$(grep "SCORE:" "$d" 2>/dev/null | tail -1)
  printf "%-26s %s\n" "$t" "$s"
done
