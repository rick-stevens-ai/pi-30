"""kv backend: flat {str:str} <-> "k1=v1;k2=v2" (stdlib only)."""


_DSEP = ";"  # separator between pairs
_KSEP = "="  # separator inside each pair.


def dumps(obj):
    """Dump a flat dict of str->str to 'k1=v1;k2=v2'."""
    if obj is None:
        return ""
    parts = []
    for k, v in obj.items():
        parts.append(f"{k}{_KSEP}{v}")
    return _DSEP.join(parts)


def loads(s):
    """Load a 'k1=v1;k2=v2' string back into {"k1": "v1", "k2": "v2"}."""
    s = s.strip() if isinstance(s, str) else s
    if not s:
        return {}
    result = {}
    for pair in s.split(_DSEP):
        if _KSEP in pair:
            k, v = pair.split(_KSEP, 1)
            result[k] = v
    return result

