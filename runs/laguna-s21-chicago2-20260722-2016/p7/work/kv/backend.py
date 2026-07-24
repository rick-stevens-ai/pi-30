"""kv backend: parse "k1=v1;k2=v2" -> {"k1": "v1", "k2": "v2"}."""


def parse(text: str) -> dict:
    result = {}
    for entry in text.split(";"):
        entry = entry.strip()
        if not entry:
            continue
        if "=" not in entry:
            continue
        key, value = entry.split("=", 1)
        result[key.strip()] = value.strip()
    return result