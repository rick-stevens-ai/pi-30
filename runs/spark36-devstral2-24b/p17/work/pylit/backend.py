"""
Pylit backend for serialization/deserialization using Python literals.

This module implements the pylit format:
- any literal type (int, float, str, list, dict, etc.)
- dumps uses repr(obj)
- loads uses ast.literal_eval(s)
"""

import ast
from typing import Any


def dumps(obj: Any) -> str:
    """Serialize object to string using Python literal representation.
    
    Args:
        obj: Object to serialize (any Python literal type)
        
    Returns:
        String representation using repr()
    """
    return repr(obj)


def loads(s: str) -> Any:
    """Deserialize string back to object using ast.literal_eval.
    
    Args:
        s: String to deserialize (must be a valid Python literal)
        
    Returns:
        Deserialized object
    """
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid literal string: {s}") from e
