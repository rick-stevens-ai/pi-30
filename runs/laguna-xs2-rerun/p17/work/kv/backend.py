"""KV backend serializer.

kv: flat {str:str} <-> "k1=v1;k2=v2"
"""


def dumps(obj) -> str:
    """Serialize flat {str:str} dict to "k1=v1;k2=v2"."""
    return ";".join(f"{k}={v}" for k, v in obj.items())


def loads(s) -> dict:
    """Deserialize "k1=v1;k2=v2" to flat {str:str} dict."""
    result = {}
    for pair in s.split(";"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            result[k] = v
    return result