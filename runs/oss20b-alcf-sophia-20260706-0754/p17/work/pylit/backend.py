"""pylit backend.

This backend serialises any Python literal using :func:`repr` and deserialises
with :func:`ast.literal_eval`.

The module exposes two functions:

* ``dumps(obj)`` -> ``str``  : returns ``repr(obj)``.
* ``loads(s)``   -> ``obj``  : parses via :func:`ast.literal_eval`.

Only the standard library is used – no ``eval`` is ever executed.
"""

from __future__ import annotations

import ast

__all__ = ["dumps", "loads"]


def dumps(obj) -> str:
    """Return the Python literal representation of *obj*.

    Parameters
    ----------
    obj:
        Any value that is representable as a Python literal.

    Returns
    -------
    str
        The ``repr`` of *obj*.
    """
    return repr(obj)


def loads(s: str):
    """Parse a Python literal string.

    Parameters
    ----------
    s : str
        A string produced by :func:`dumps`.

    Returns
    -------
    object
        The Python object represented by *s*.

    Raises
    ------
    (Various)
        ``ast.literal_eval`` may raise ``ValueError`` or ``SyntaxError`` if
        *s* is not a valid Python literal.
    """
    return ast.literal_eval(s)

*** End of file ***