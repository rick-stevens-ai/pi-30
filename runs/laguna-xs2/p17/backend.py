"""Backend for kv format: flat {str:str} <-> 'k1=v1;k2=v2'."""

def dumps(obj: dict) -> str:
    """Serialize a flat {str:str} dict to 'k1=v1;k2=v2' format."""
    if not isinstance(obj, dict):
        raise TypeError("kv.dumps expects a dict")
    pairs = [f"{k}={v}" for k, v in obj.items()]
    return ";".join(pairs)


def loads(s: str) -> dict:
    """Deserialize 'k1=v1;k2=v2' format to a flat {str:str} dict."""
    if not s:
        return {}
    result = {}
    for pair in s.split(";"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            result[k] = v
    return result