"""kv backend: parse 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}.

Stdlib only.
"""


def parse(text: str) -> dict:
    result = {}
    if text is None:
        return result
    stripped = text.strip()
    if stripped == "":
        return result
    for pair in stripped.split(";"):
        if pair == "":
            continue
        if "=" not in pair:
            continue
        key, _, value = pair.partition("=")
        result[key] = value
    return result
