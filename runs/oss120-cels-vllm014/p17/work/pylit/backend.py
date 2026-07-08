"""Pylit backend for serialization.

Provides simple dump/load using Python literal representation.
`dumps` returns ``repr(obj)`` and `loads` parses the string using
`ast.literal_eval`, which safely evaluates Python literals without
executing arbitrary code.
"""

import ast

__all__ = ["dumps", "loads"]


def dumps(obj):
    """Serialize ``obj`` to a string using ``repr``.

    Args:
        obj: Any Python object that has a literal representation.
    Returns:
        str: The ``repr`` of the object.
    """
    return repr(obj)


def loads(s):
    """Deserialize a string produced by :func:`dumps`.

    Uses :func:`ast.literal_eval` to safely evaluate the literal.
    Args:
        s (str): The string representation.
    Returns:
        The Python object represented by ``s``.
    """
    return ast.literal_eval(s)
