"""pylit backend: serialize any Python literal via repr / ast.literal_eval.

Stdlib only; never uses eval().
"""

import ast


def dumps(obj) -> str:
    """Return a string representation of a Python literal."""
    return repr(obj)


def loads(s: str):
    """Parse a Python literal string safely using ast.literal_eval."""
    return ast.literal_eval(s)
