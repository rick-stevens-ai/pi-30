import ast

def dumps(obj):
    """Convert a Python literal object to its string representation."""
    return repr(obj)

def loads(s):
    """Parse a string representing a Python literal into an object."""
    return ast.literal_eval(s)
