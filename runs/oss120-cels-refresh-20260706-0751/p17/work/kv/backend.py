"""kv backend serializer.

Provides two simple functions:
    - ``dumps(obj)`` converts a flat ``dict`` of ``str`` keys and ``str`` values
      into a semicolon‑separated ``k=v`` string.
    - ``loads(s)`` parses such a string back into a ``dict``.

The format is deliberately simple:
    * Keys and values are stringified using ``str()``.
    * Pairs are joined by ``;``; an empty dictionary yields an empty string.
    * Within a pair the key and value are separated by ``=``.
    * No escaping is performed – this backend is intended for simple, flat
      data where keys/values do not contain ``;`` or ``=``.
"""

from __future__ import annotations

from typing import Dict

__all__ = ["dumps", "loads"]


def dumps(obj: Dict[str, str]) -> str:
    """Serialize a flat ``dict`` of ``str`` keys/values to ``k=v;k=v`` format.

    Parameters
    ----------
    obj:
        Mapping of keys to values. Both keys and values will be coerced to
        ``str`` via ``str()`` before formatting.

    Returns
    -------
    str
        A semicolon‑separated list of ``key=value`` pairs. The ordering follows
        the iteration order of the provided ``dict`` (preserves insertion order
        for Python 3.7+).
    """
    if not obj:
        return ""
    # Build each ``k=v`` chunk; ensure both parts are strings.
    parts = [f"{str(k)}={str(v)}" for k, v in obj.items()]
    return ";".join(parts)


def loads(s: str) -> Dict[str, str]:
    """Parse a ``k=v;k=v`` string back into a ``dict``.

    Empty input returns an empty ``dict``. Whitespace surrounding keys or values
    is stripped. Duplicate keys are overwritten by the later occurrence, mimicking
    the behaviour of successive assignments in a typical ``kv`` format.
    """
    result: Dict[str, str] = {}
    if not s:
        return result
    # Split on ';' – ignore empty chunks that may arise from trailing ';'.
    for pair in filter(None, s.split(";")):
        # Split only on the first '=', allowing values to contain additional
        # '=' characters (they will be preserved as part of the value).
        if "=" not in pair:
            # If there is no '=', treat the whole token as a key with an empty
            # value. This mirrors a permissive parser and keeps the function
            # robust against malformed input.
            key, value = pair, ""
        else:
            key, value = pair.split("=", 1)
        result[key.strip()] = value.strip()
    return result
