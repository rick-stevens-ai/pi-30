"""KV backend parser.

Implements the shared interface required by the planner:
    parse(text: str) -> dict

The parser accepts a string of semicolon‑separated key/value pairs, where each
pair is of the form ``key=value``. Whitespace around keys, values and separators
is ignored. An empty input string yields an empty dictionary.

Example
-------
>>> parse('k1=v1;k2=v2')
{'k1': 'v1', 'k2': 'v2'}
"""

from __future__ import annotations


def parse(text: str) -> dict[str, str]:
    """Parse a ``key=value``;``key=value`` string into a dictionary.

    Parameters
    ----------
    text:
        The input string containing ``key=value`` pairs separated by semicolons.
        Empty strings or strings containing only whitespace result in an empty
        dictionary.

    Returns
    -------
    dict
        Mapping of keys to their corresponding values.
    """
    # Trim surrounding whitespace; early‑return for empty input.
    stripped = text.strip()
    if not stripped:
        return {}

    result: dict[str, str] = {}
    # Split on semicolons; ignore empty segments that may appear due to a
    # trailing semicolon.
    for pair in stripped.split(';'):
        if not pair:
            continue
        # Split only on the first '=' to allow values that may contain '='.
        if '=' not in pair:
            # If there is no '=', treat the whole segment as a key with an
            # empty string value (mirrors typical KV parsing behaviour).
            key, value = pair.strip(), ""
        else:
            key, value = pair.split('=', 1)
            key, value = key.strip(), value.strip()
        result[key] = value
    return result
