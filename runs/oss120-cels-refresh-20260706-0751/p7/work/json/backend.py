"""JSON backend parser.

Implements the shared interface required by the planner:
    parse(text: str) -> dict

The parser accepts a string representing a JSON object and returns the
corresponding ``dict`` using the Python standard‑library ``json`` module.
No additional validation is performed – the caller is expected to provide a
valid JSON object string. If the parsed JSON is not a mapping, a ``TypeError``
is raised to keep the behaviour consistent with the other backends which
always return a ``dict``.

Example
-------
>>> parse('{"x": 1, "y": [2, 3]}')
{'x': 1, 'y': [2, 3]}
"""

from __future__ import annotations
import importlib
_json = importlib.import_module('json')
from typing import Any, Mapping


def parse(text: str) -> dict:
    """Parse a JSON object string into a Python ``dict``.

    Parameters
    ----------
    text:
        A JSON‑encoded string that must represent an object (i.e. a mapping).

    Returns
    -------
    dict
        The decoded JSON object.

    Raises
    ------
    json.JSONDecodeError
        If ``text`` is not valid JSON.
    TypeError
        If the decoded JSON value is not a mapping (e.g. a list or primitive).
    """
    # The standard library ``json`` module parses the string. ``object_hook``
    # is not needed because the default behaviour already yields ``dict``
    # for JSON objects.
    parsed: Any = _json.loads(text)
    if not isinstance(parsed, Mapping):
        raise TypeError("JSON input must decode to a mapping (object)")
    # ``parsed`` is a ``dict`` subclass (usually ``dict``); cast to ``dict`` for
    # a clean return type.
    return dict(parsed)
