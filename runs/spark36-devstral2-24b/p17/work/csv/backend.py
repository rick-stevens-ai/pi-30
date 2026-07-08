"""
CSV backend for serialization/deserialization.

This module implements two formats:
1. csv: obj {'fields': [...]} <-> 'a,b,c'
2. kv: flat {str: str} <-> 'k1=v1; k2=v2'
3. pylit: any literal, dumps=repr(obj), loads=ast.literal_eval(s)

Stdlib only - no external dependencies.
"""

import ast
from typing import Any, Dict, List, Union


def dumps(obj: Any) -> str:
    """Serialize object to string based on its type.
    
    Args:
        obj: Object to serialize. Can be dict with 'fields' key for CSV format,
             dict with string keys/values for KV format, or any literal for pylit.
    
    Returns:
        Serialized string representation
    """
    if isinstance(obj, dict):
        # Check if this is a CSV format object (has 'fields' key)
        if 'fields' in obj:
            # CSV format: {'fields': [...]} -> 'a,b,c'
            fields = obj['fields']
            if not all(isinstance(field, str) for field in fields):
                raise ValueError("All fields must be strings for CSV format")
            return ','.join(fields)
        else:
            # KV format: flat {str: str} -> 'k1=v1; k2=v2'
            if not all(isinstance(k, str) and isinstance(v, str) for k, v in obj.items()):
                raise ValueError("All keys and values must be strings for KV format")
            return '; '.join(f'{k}={v}' for k, v in obj.items())
    else:
        # pylit format: any literal -> repr(obj)
        return repr(obj)


def loads(s: str) -> Any:
    """Deserialize string back to object.
    
    Args:
        s: String to deserialize. Format is detected automatically:
           - If contains only commas and strings: CSV format
           - If contains '=' separators: KV format  
           - Otherwise: pylit format (ast.literal_eval)
    
    Returns:
        Deserialized object
    """
    s = s.strip()
    
    # Detect CSV format: string looks like comma-separated values
    # (contains commas, no '=' separators, and passes basic validation)
    if ',' in s and not ('=' in s and not s.startswith('{') and not s.endswith('}')):
        # Parse CSV format
        parts = [p.strip() for p in s.split(',')]
        return {'fields': parts}
    
    # Detect KV format: contains '=' signs
    if '=' in s:
        # Parse KV format
        result = {}
        for pair in s.split('; '):
            pair = pair.strip()
            if not pair:
                continue
            if '=' not in pair:
                raise ValueError(f"Invalid KV pair: {pair}")
            key, value = pair.split('=', 1)
            result[key.strip()] = value.strip()
        return result
    
    # pylit format: use ast.literal_eval
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid literal string: {s}") from e
