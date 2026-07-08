"""Backend parser for simple key-value (kv) strings.

The module provides a single public function ``parse`` that converts a
kv‑formatted string into a Python ``dict``.

Supported format
----------------
* ``k1=v1;k2=v2`` – keys and values are separated by ``=`` and each pair
  by ``;``.
* Whitespace around keys, values and separators is ignored.
* Empty input returns an empty ``dict``.

The implementation relies only on the Python standard library and does not
perform any type conversion – values are returned as strings.
"""

from __future__ import annotations

from typing import Dict


def parse(text: str) -> Dict[str, str]:
    """Parse a ``kv`` formatted string into a dictionary.

    Parameters
    ----------
    text:
        The kv string, e.g. ``"k1=v1;k2=v2"``.

    Returns
    -------
    dict:
        Mapping of keys to their corresponding string values.
    """
    result: Dict[str, str] = {}
    if not text:
        return result

    # Split into pairs separated by ';'. Filter out empty segments that may
    # appear due to trailing semicolons.
    pairs = [pair for pair in text.split(";") if pair.strip()]
    for pair in pairs:
        if "=" not in pair:
            # If there is no '=', we treat the whole segment as a key with an
            # empty string value.
            key = pair.strip()
            value = ""
        else:
            key, value = pair.split("=", 1)
            key = key.strip()
            value = value.strip()
        # Only add non‑empty keys – an empty key would be ambiguous.
        if key:
            result[key] = value
    return result
