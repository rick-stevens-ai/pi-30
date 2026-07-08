# kv backend: flat {str:str} <-> "k1=v1;k2=v2"
# stdlib only

def dumps(obj: dict) -> str:
    """Serialize a flat dict of str->str to 'k1=v1;k2=v2' format."""
    if not isinstance(obj, dict):
        raise TypeError("kv.dumps expects a dict")
    for k, v in obj.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise TypeError("kv.dumps expects flat {str:str} dict")
    return ";".join(f"{k}={v}" for k, v in obj.items())


def loads(s: str) -> dict:
    """Deserialize 'k1=v1;k2=v2' format to a flat dict of str->str."""
    if not s:
        return {}
    result = {}
    for pair in s.split(";"):
        if "=" not in pair:
            raise ValueError(f"Invalid kv pair: {pair}")
        k, v = pair.split("=", 1)
        result[k] = v
    return result