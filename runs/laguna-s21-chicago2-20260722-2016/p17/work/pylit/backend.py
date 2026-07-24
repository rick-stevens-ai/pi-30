"""pylit backend: serialize any Python literal via repr/ast.literal_eval.

Stdlib only. Never uses eval().
"""

import ast


def dumps(obj) -> str:
    """Serialize a Python literal to its repr string."""
    return repr(obj)


def loads(s) -> object:
    """Deserialize a Python literal string safely via ast.literal_eval."""
    return ast.literal_eval(s)