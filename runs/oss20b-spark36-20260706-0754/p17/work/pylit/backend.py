"""
Backend for the *pylit* serializer.

A ``pylit`` backend simply serialises an arbitrary Python object by using its
``repr()`` representation and then deserialising it with :func:`ast.literal_eval`.
This is intentionally *safe*: the standard library implementation of
``literal_eval`` only accepts literals (strings, numbers, tuples, lists,
dicts, booleans, ``None``).  No ``eval`` or similar unsafe constructs are used.

The backend exports two functions required by the `plan.md`:

* ``dumps(obj) -> str`` – return a ``repr`` string that can be round‑tripped by
  :func:`loads`.
* ``loads(s: str) -> object`` – reconstruct an object from its ``repr()``
  string.
"""
from __future__ import annotations

import ast
from typing import Any

__all__: list[str] = ["dumps", "loads"]


def dumps(obj: Any) -> str:
    """Return a ``repr`` string that can be round‑tripped by :func:`loads`.

    Parameters
    ----------
    obj:
        The Python object to serialise.  It must consist only of literals that
        :func:`ast.literal_eval` understands.
    """
    return repr(obj)


def loads(s: str) -> Any:
    """Return an object from a string produced by :func:`dumps`.

    Parameters
    ----------
    s:
        A string created earlier by ``dumps``.  It must be a valid Python
        literal.

    Raises
    ------
    ValueError or SyntaxError
        Propagated from :func:`ast.literal_eval` when *s* is not a literal.
    """
    return ast.literal_eval(s)
