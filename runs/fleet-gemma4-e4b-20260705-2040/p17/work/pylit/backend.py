import ast

def dumps(obj):
    """Dumps a Python object to its string representation."""
    return repr(obj)

def loads(s):
    """Loads a Python literal from a string using ast.literal_eval."""
    try:
        # Use ast.literal_eval for safe evaluation of Python literals
        return ast.literal_eval(s)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Failed to safely evaluate string '{s}' as a Python literal: {e}")

