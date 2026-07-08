import ast

class PylitBackend:
    """
    Implements the pylit backend for serialization/deserialization.
    dumps(obj) -> str: Uses repr(obj)
    loads(s) -> obj: Uses ast.literal_eval(s)
    """
    def dumps(self, obj) -> str:
        """Serializes an object using its string representation."""
        return repr(obj)

    def loads(self, s: str):
        """Deserializes a string back into a Python object using ast.literal_eval."""
        # Stdlib only, never eval
        return ast.literal_eval(s)

# Assuming the system expects an instance or module-level functions.
# For simplicity in this context, we'll expose them directly if that fits the structure, 
# but defining a class is cleaner. Let's assume the file needs to export these functions/methods.

def dumps(obj):
    return repr(obj)

def loads(s):
    import ast
    return ast.literal_eval(s)