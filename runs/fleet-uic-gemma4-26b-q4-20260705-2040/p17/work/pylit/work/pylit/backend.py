import ast

def dumps(obj) -> str:
    """Serializes a Python literal to a string using repr()."""
    return repr(obj)

def loads(s: str):
    """Deserializes a string into a Python literal using ast.literal_eval()."""
    return ast.literal_eval(s)
