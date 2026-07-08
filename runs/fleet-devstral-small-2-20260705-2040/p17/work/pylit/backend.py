"""
Pylit backend implementation.

This module provides serialization/deserialization for pylit format:
- dumps(obj) -> str: uses repr() to serialize any Python literal
- loads(s) -> obj: uses ast.literal_eval() to deserialize (safe, stdlib only)

Supported types: int, float, str, bool, None, list, tuple, dict
"""

from ast import literal_eval


def dumps(obj):
    """
    Serialize an object to a pylit string using repr().
    
    Args:
        obj: Any Python literal (int, float, str, bool, None, list, tuple, dict)
    
    Returns:
        str: Pylit representation of the object
    """
    return repr(obj)


def loads(s):
    """
    Deserialize a pylit string to an object using ast.literal_eval().
    
    Args:
        s (str): Pylit string to deserialize
    
    Returns:
        obj: Deserialized Python object
    
    Raises:
        ValueError: If the string contains invalid pylit syntax
    """
    return literal_eval(s)
