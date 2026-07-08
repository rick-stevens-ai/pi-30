"""pylit backend — repr / ast.literal_eval serialization (stdlib only)."""

import ast


def dumps(obj):
    """Serialize *obj* to a string using repr."""
    return repr(obj)


def loads(s):
    """Deserialize a string *s* using ast.literal_eval (never eval)."""
    return ast.literal_eval(s)
