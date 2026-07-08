"""pylit backend: Python literal serialization using stdlib ast."""

import ast


def dumps(obj) -> str:
    """Serialize a Python object to string using repr()."""
    return repr(obj)


def loads(s) -> object:
    """Deserialize a string to Python object using ast.literal_eval()."""
    return ast.literal_eval(s)