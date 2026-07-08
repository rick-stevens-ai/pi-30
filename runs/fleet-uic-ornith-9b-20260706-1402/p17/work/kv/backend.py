"""KV backend:  flat {str:str} <-> "k1=v1;k2=v2"  (stdlib only)."""


def dumps(obj):
    return ";".join(f"{k}={v}" for k, v in obj.items())


def loads(s):
    if not s:
        return {}
    result = {}
    for pair in s.split(";"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            result[k] = v
    return result
