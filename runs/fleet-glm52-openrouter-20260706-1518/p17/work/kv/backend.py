"""kv backend: flat {str:str} <-> 'k1=v1;k2=v2'."""

from typing import Dict


def dumps(obj: Dict[str, str]) -> str:
    """Serialize a flat {str:str} dict to 'k1=v1;k2=v2'."""
    if not isinstance(obj, dict):
        raise TypeError("kv.dumps expects a dict, got %r" % type(obj).__name__)
    parts = []
    for k, v in obj.items():
        if not isinstance(k, str):
            raise TypeError("kv.dumps keys must be str, got %r" % type(k).__name__)
        if not isinstance(v, str):
            raise TypeError("kv.dumps values must be str, got %r" % type(v).__name__)
        if "=" in k:
            raise ValueError("kv.dumps keys must not contain '=': %r" % k)
        if ";" in k or ";" in v:
            raise ValueError("kv.dumps keys/values must not contain ';': %r" % k)
        parts.append("%s=%s" % (k, v))
    return ";".join(parts)


def loads(s: str) -> Dict[str, str]:
    """Parse 'k1=v1;k2=v2' back into a flat {str:str} dict."""
    if not isinstance(s, str):
        raise TypeError("kv.loads expects a str, got %r" % type(s).__name__)
    result: Dict[str, str] = {}
    if s == "":
        return result
    for part in s.split(";"):
        if "=" not in part:
            raise ValueError("kv.loads: malformed segment %r" % part)
        k, v = part.split("=", 1)
        result[k] = v
    return result
