"""
Pylit backend for serialization/deserialization using Python literals.

Implements dumps and loads per PLAN.md:
- dumps: uses repr() to produce a string representation of any Python literal.
- loads: parses the string safely with ast.literal_eval (stdlib only).
"""

import ast
from typing import Any


def dumps(obj: Any) -> str:
    """Serialize a Python literal to its string representation.

    Args:
        obj: Any Python literal (int, float, str, list, dict, tuple, etc.)
    Returns:
        The ``repr`` of the object.
    """
    return repr(obj)


def loads(s: str) -> Any:
    """Deserialize a string produced by ``dumps`` back to a Python object.

    Uses ``ast.literal_eval`` for safe evaluation – only literal structures are allowed.
    Raises ``ValueError`` if the string cannot be parsed as a literal.
    """
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid literal string: {s}") from e
