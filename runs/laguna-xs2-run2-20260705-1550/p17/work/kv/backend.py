"""kv backend: flat {str:str} <-> 'k1=v1;k2=v2'"""


def dumps(obj: dict) -> str:
    """Serialize a flat dict to 'k1=v1;k2=v2' format."""
    return ";".join(f"{k}={v}" for k, v in obj.items())


def loads(s: str) -> dict:
    """Deserialize 'k1=v1;k2=v2' to a flat dict."""
    if not s:
        return {}
    return dict(pair.split("=", 1) for pair in s.split(";"))