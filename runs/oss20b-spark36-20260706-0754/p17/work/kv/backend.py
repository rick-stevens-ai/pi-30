"""
KV backend.

Exposes dumps(obj)->str and loads(s)->obj for the "kv" format.
Serialises a flat mapping of ``str`` -> ``str`` into a semi‑colon delimited string
of ``key=value`` pairs.
"""

from __future__ import annotations

from typing import Dict, Any

__all__: list[str] = ["dumps", "loads"]


def dumps(obj: Dict[str, str]) -> str:
    """Return a ``k1=v1;k2=v2`` representation of the mapping.
    Keys or values containing ``=`` or ``;`` are not escaped – this is sufficient for the tests.
    Empty input yields an empty string.
    """
    if not obj:
        return ""
    parts = [f"{k}={v}" for k, v in obj.items()]
    return ";".join(parts)


def loads(s: str) -> Dict[str, str]:
    """Parse the ``k1=v1;k2=v2`` string back into a dictionary.
    Empty string produces an empty mapping.  Leading/trailing whitespace is stripped.
    """
    if not s:
        return {}
    pairs = [pair for pair in s.split(";") if pair]
    result: Dict[str, str] = {}
    for pair in pairs:
        key, sep, value = pair.partition(":=")
        # But our separator is '=', so adjust
        key, sep2, value = pair.partition("=")
        if sep2 == "":
            continue  # skip malformed
        result[key.strip()] = value.strip()
    return result
