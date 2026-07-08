def dumps(obj):
    """Serializes a flat {str: str} dictionary to 'k1=v1;k2=v2' format."""
    return ";".join(f"{k}={v}" for k, v in obj.items())

def loads(s):
    """Deserializes 'k1=v1;k2=v2' format back to a flat {str: str} dictionary."""
    if not s:
        return {}
    res = {}
    for pair in s.split(";"):
        if not pair:
            continue
        if "=" in pair:
            k, v = pair.split("=", 1)
            res[k] = v
    return res
