"""
JSON backend for parsing JSON objects.

This module exposes a single function `parse` which accepts a string containing a valid
JSON object and returns the corresponding Python dictionary using the standard
library's :mod:`json` module. It simply delegates to :func:`json.loads`.

The interface is intentionally minimal: only ``parse`` is exported, and any JSON
syntax errors will propagate as :class:`json.JSONDecodeError`, which is the
expected behaviour for callers of this backend.
"""

import json

def parse(text: str) -> dict:
    """Parse a JSON object string into a Python dictionary.

    Parameters
    ----------
    text: str
        A string representing a JSON object, e.g. ``'{"a": 1, "b": 2}'``.

    Returns
    -------
    dict
        The parsed key/value mapping.
    """
    return json.loads(text)
