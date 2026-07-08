"""pylit backend: serialize any Python literal using repr/ast.literal_eval."""
import ast


def dumps(obj) -> str:
    """Serialize a Python literal to its repr string."""
    return repr(obj)


def loads(s: str):
    """Deserialize a Python literal from its repr string using ast.literal_eval."""
    return ast.literal_eval(s)
