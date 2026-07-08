import json


def parse(text: str):
    """Parse a string into a dictionary.

    The function supports three simple formats:
    * JSON object string – parsed with :mod:`json`.
    * CSV – a comma‑separated list like ``"a,b,c"``. The result is
      ``{"fields": ["a", "b", "c"]}``.
    * KV – a semicolon‑separated list of ``key=value`` pairs like
      ``"k1=v1;k2=v2"``. The result is a mapping of the keys to values.

    The function tries JSON first; if that fails it falls back to KV
    detection (requires both ``=`` and ``;``) and finally treats the input
    as CSV.
    """
    # Try JSON parsing first – this is the most strict format.
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
        # If JSON parses but is not a dict, we still return it as‑is
        # because the contract says "JSON object string" – otherwise it
        # would be considered an unsupported format.
        return obj
    except json.JSONDecodeError:
        pass

    # KV format detection: contains at least one '=' and uses ';' as separator.
    if "=" in text and ";" in text:
        result = {}
        # Split on ';' but ignore empty trailing part if the string ends with ';'
        pairs = [p for p in text.split(";") if p]
        for pair in pairs:
            if "=" not in pair:
                # malformed pair – skip it
                continue
            key, value = pair.split("=", 1)
            result[key.strip()] = value.strip()
        return result

    # Fallback to CSV – split on commas.
    fields = [field.strip() for field in text.split(",") if field]
    return {"fields": fields}
