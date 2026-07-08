def dumps(obj: dict[str, str]) -> str:
    """
    Serializes a flat dictionary {str: str} to a string "k1=v1;k2=v2".
    """
    return ";".join(f"{k}={v}" for k, v in obj.items())

def loads(s: str) -> dict[str, str]:
    """
    Deserializes a string "k1=v1;k2=v2" to a flat dictionary {str: str}.
    """
    if not s:
        return {}
    result = {}
    pairs = s.split(";")
    for pair in pairs:
        if "=" in pair:
            k, v = pair.split("=", 1)
            result[k] = v
    return result
