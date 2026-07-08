import ast

def dumps(obj) -> str:
    """
    Serializes any python literal to its repr string.
    """
    return repr(obj)

def loads(s: str):
    """
    Deserializes a repr string back into a python literal using ast.literal_eval.
    """
    return ast.literal_eval(s)
