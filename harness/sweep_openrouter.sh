#!/usr/bin/env bash
# OpenRouter free-tier full-10 tool-use sweep.
# Verdicts off verifier exit codes only. fleet=openrouter.
set -u
export PATH="/Users/stevens/.nvm/versions/node/v24.16.0/bin:$PATH"
cd /Users/stevens/pi-problems-30

PROVIDER="openrouter-free"
# Tool-use-capable free models (skip dolphin/hermes-405b = flaky/no native tools)
MODELS=(
  "qwen/qwen3-coder:free|or-qwen3coder"
  "openai/gpt-oss-120b:free|or-gptoss120b"
  "nvidia/nemotron-3-super-120b-a12b:free|or-nemotron-super"
  "qwen/qwen3-next-80b-a3b-instruct:free|or-qwen3next80b"
  "google/gemma-4-31b-it:free|or-gemma4-31b"
)

for entry in "${MODELS[@]}"; do
  model="${entry%%|*}"
  tag="${entry##*|}"
  echo "######## $tag ($model) $(date) ########"
  bash run_model.sh "$PROVIDER" "$model" "$tag" 2>&1
  echo "######## $tag DONE $(date) ########"
done
echo "ALL OPENROUTER SWEEPS DONE $(date)"
