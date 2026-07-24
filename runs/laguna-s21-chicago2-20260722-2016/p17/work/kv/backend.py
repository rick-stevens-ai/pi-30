"""kv backend: flat {str:str} <-> "k1=v1;k2=v2".

dumps(obj) -> str : serialize a flat string->string dict to "k1=v1;k2=v2".
loads(s)   -> obj : parse "k1=v1;k2=v2" back into the dict.

Round-trip: loads(dumps(d)) == d for any flat {str:str} dict.
Stdlib only.
"""


def dumps(obj) -> str:
    """Serialize a flat {str:str} dict to "k1=v1;k2=v2".

    Empty dict -> "".  Keys/values are joined with "=" and pairs with ";".
    """
    return ";".join("{}={}".format(k, v) for k, v in obj.items())


def loads(s: str) -> dict:
    """Parse "k1=v1;k2=v2" into a {str:str} dict.

    "" -> {}.  Each pair is split on the first "=" so values may contain "=".
    """
    result = {}
    for pair in s.split(";"):
        if not pair:
            continue
        k, v = pair.split("=", 1)
        result[k] = v
    return result