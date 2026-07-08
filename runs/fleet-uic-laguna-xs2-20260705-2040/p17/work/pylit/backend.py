import ast


def dumps(obj) -> str:
    """Serialize a Python literal to string using repr()."""
    return repr(obj)


def loads(s) -> object:
    """Deserialize a string to Python literal using ast.literal_eval()."""
    return ast.literal_eval(s)