"""kv backend: serialize flat str->str dict as 'k1=v1;k2=v2'."""


def dumps(obj: dict[str, str]) -> str:
    """Serialize a flat str->str dict to 'k1=v1;k2=v2' format."""
    return ";".join(f"{k}={v}" for k, v in obj.items())


def loads(s: str) -> dict[str, str]:
    """Deserialize 'k1=v1;k2=v2' format to a flat str->str dict."""
    if not s:
        return {}
    result = {}
    for pair in s.split(";"):
        if pair:
            k, v = pair.split("=", 1)
            result[k] = v
    return result
