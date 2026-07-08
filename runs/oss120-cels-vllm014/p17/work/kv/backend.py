"""kv backend: simple key=value pairs separated by semicolons.

Provides two functions:
    dumps(obj) -> str
    loads(s)   -> obj

- ``obj`` is a flat dictionary mapping strings to strings.
- ``dumps`` serialises ``obj`` to a single string of the form ``"k1=v1;k2=v2"``.
- ``loads`` parses such a string back into a dict.

Both functions are deliberately tiny and use only the Python standard library.
"""

def dumps(obj: dict) -> str:
    """Serialise a flat ``{str: str}`` dictionary to a ``"k=v;..."`` string.

    The order of items is the insertion order of the dict (Python 3.7+ preserves order).
    An empty dict produces an empty string.
    """
    if not obj:
        return ""
    # Ensure keys and values are strings; rely on ``str`` conversion for safety.
    return ";".join(f"{str(k)}={str(v)}" for k, v in obj.items())


def loads(s: str) -> dict:
    """Parse a ``"k=v;..."`` string back into a dictionary.

    Empty input returns an empty dict. Duplicate keys are allowed; the later
    occurrence wins, mirroring typical ``dict`` behaviour when updating.
    """
    if not s:
        return {}
    result = {}
    for pair in s.split(";"):
        if not pair:
            continue
        # Split on the first '=' only, allowing '=' in the value.
        key, value = pair.split("=", 1)
        result[key] = value
    return result
