'''kv backend serializer

Provides two functions:
    dumps(obj) -> str
    loads(s)   -> obj

The kv format is a simple flat mapping of string keys to string values
encoded as ``k1=v1;k2=v2``.  An empty mapping is represented by the empty
string.  Keys and values are not quoted; they are converted to ``str``
using ``str()`` when dumping.  When loading, the raw substrings before the
first ``=`` and after the first ``=`` in each ``key=value`` pair are used as
the dictionary key and value respectively.

Only the standard library is used.
''' 

def dumps(obj: dict) -> str:
    """Serialize a flat ``{str: str}`` mapping to a ``k=v`` string.

    The function accepts any mapping whose keys and values can be cast to
    ``str``.  The resulting order reflects the insertion order of the input
    dictionary (Python 3.7+ guarantees order preservation).
    """
    if not obj:
        return ""
    parts = []
    for k, v in obj.items():
        # Ensure keys and values are strings – the spec says they already are,
        # but ``str`` conversion makes the function robust.
        parts.append(f"{str(k)}={str(v)}")
    return ";".join(parts)


def loads(s: str) -> dict:
    """Deserialize a ``k=v`` string into a flat ``{str: str}`` mapping.

    An empty string yields an empty dictionary.  Pairs are separated by ``;``.
    The first ``=`` in each pair separates the key from the value.  Duplicate
    keys are allowed – the last occurrence wins, mirroring the behaviour of
    ``dict.update``.
    """
    result = {}
    if not s:
        return result
    # Split on ';' – empty segments (e.g., trailing ';') are ignored.
    for pair in s.split(';'):
        if not pair:
            continue
        if '=' not in pair:
            # A malformed pair; raise a ValueError to be consistent with
            # typical parsing failures.
            raise ValueError(f"Invalid kv pair without '=': {pair!r}")
        key, value = pair.split('=', 1)
        result[key] = value
    return result
