"""kv backend: flat {str:str} <-> 'k1=v1;k2=v2'"""


def dumps(obj: dict) -> str:
    """Serialize a flat string-to-string dict to 'k1=v1;k2=v2'."""
    return ";".join(f"{k}={v}" for k, v in obj.items())


def loads(s: str) -> dict:
    """Deserialize 'k1=v1;k2=v2' to a flat string-to-string dict."""
    result = {}
    for pair in s.split(";"):
        if not pair:
            continue
        k, v = pair.split("=", 1)
        result[k] = v
    return result
