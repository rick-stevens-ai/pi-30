import ast

def dumps(obj):
    """
    Return a string representation of any Python literal object using repr().
    This matches the pylit backend specification.
    """
    return repr(obj)

def loads(s):
    """
    Parse a string containing a Python literal or container display,
    returning the corresponding Python object. Only stdlib ast.literal_eval is used,
    never eval().
    """
    return ast.literal_eval(s)