import json
import csv
from io import StringIO
from typing import Dict, Any

def parse(text: str) -> Dict[str, Any]:
    """
    Parses input text based on format (CSV, KV, JSON).
    Prioritizes detection heuristics.
    """
    text = text.strip()

    # 1. Try CSV parsing (if it contains commas and looks like a single row)
    if ',' in text and not ('=' in text or '{' in text):
        try:
            fields = [field.strip() for field in text.split(',')]
            return {"fields": fields}
        except Exception:
            # Fall through to other parsers if splitting fails unexpectedly
            pass

    # 2. Try KV parsing (key=value;key2=value2)
    if ';' in text and '=' in text:
        result = {}
        pairs = text.split(';')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                result[key.strip()] = value.strip()
        return result

    # 3. Try JSON parsing
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
        else:
            raise TypeError("JSON input must be an object.")
    except json.JSONDecodeError:
        pass # Not JSON

    # If none of the above worked, return an error or default structure
    return {"error": "Could not parse text", "input": text}

if __name__ == '__main__':
    # Example tests based on requirements
    print("--- CSV Test ---")
    csv_text = 'a,b,c'
    print(f"Input: '{csv_text}' -> Output: {parse(csv_text)}")

    print("\n--- KV Test ---")
    kv_text = 'k1=v1;k2=v2'
    print(f"Input: '{kv_text}' -> Output: {parse(kv_text)}")

    print("\n--- JSON Test ---")
    json_text = '{"name": "Gemma", "version": 4}'
    print(f"Input: '{json_text}' -> Output: {parse(json_text)}")