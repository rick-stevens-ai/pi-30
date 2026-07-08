#!/opt/anaconda3/bin/python3
"""Extract the LAST fenced code block from pi's stdout and write it to a file.
Usage: extract_code.py <infile-with-pi-output> <outfile.py>
Handles ```python / ``` / ~~~ fences; falls back to whole content if no fence.
Exit 0 if something was written, 2 if input was empty.
"""
import sys, re

def extract(text):
    # prefer fenced blocks; take the LAST one (models often explain then code)
    blocks = re.findall(r"```(?:[a-zA-Z0-9_+-]*)\n(.*?)```", text, re.DOTALL)
    if not blocks:
        blocks = re.findall(r"~~~(?:[a-zA-Z0-9_+-]*)\n(.*?)~~~", text, re.DOTALL)
    if blocks:
        # choose the longest block (most likely the full solution)
        return max(blocks, key=len)
    return text

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    text = open(inp, encoding="utf-8", errors="replace").read()
    if not text.strip():
        sys.exit(2)
    code = extract(text).strip("\n")
    # strip stray tool-call markup some Ollama models emit
    for junk in ("</parameter>", "</function>", "</tool_call>", "<tool_call>",
                 "</invoke>", "<parameter", "</antml"):
        code = code.replace(junk, "")
    open(outp, "w", encoding="utf-8").write(code + "\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
