# backend.py for the 'pylit' serializer backend.
"""Pylit serializer backend.

Provides two simple functions:

* ``dumps(obj)`` – Convert any Python literal ``obj`` to a string using
  ``repr``. ``repr`` is guaranteed to produce a valid Python expression for
  built‑in literals, containers, numbers, strings, ``True``/``False``/``None``
  and nested combinations thereof.

* ``loads(s)`` – Convert the string back to a Python object using
  ``ast.literal_eval`` which safely evaluates the literal without invoking
  ``eval``. Only the standard‑library ``ast`` module is used – no third‑party
  dependencies.

The functions deliberately avoid any side effects, matching the contract
described in ``../../PLAN.md``.
"""

import ast
from typing import Any

__all__ = ["dumps", "loads"]


def dumps(obj: Any) -> str:
    """Serialize a Python literal to a string.

    The implementation simply returns ``repr(obj)`` which yields a valid
    Python literal representation for standard built‑in types.
    """
    return repr(obj)


def loads(s: str) -> Any:
    """Deserialize a string produced by :func:`dumps` back to a Python object.

    ``ast.literal_eval`` safely evaluates the expression and raises a
    ``ValueError`` or ``SyntaxError`` if the input is not a valid literal.
    """
    return ast.literal_eval(s)
