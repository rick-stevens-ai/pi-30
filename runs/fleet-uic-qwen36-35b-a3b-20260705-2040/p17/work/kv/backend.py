def dumps(obj: dict) -> str:
    """Flat {str:str} -> "k1=v1;k2=v2"."""
    return ";".join(f"{k}={v}" for k, v in obj.items())


def loads(s: str) -> dict:
    '"k1=v1;k2=v2" -> {"k1":"v1","k2":"v2"}'
    result = {}
    if not s:
        return result
    for pair in s.split(";"):
        k, v = pair.split("=", 1)
        result[k] = v
    return result
