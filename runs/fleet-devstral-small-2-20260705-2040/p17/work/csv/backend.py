"""
CSV backend implementation.

Exposes:
- dumps(obj) -> str: Serializes an object to CSV format
- loads(s) -> obj: Deserializes a CSV string to an object

Supported formats:
- csv: obj {'fields': [...]}
  - dumps: 'a,b,c'
  - loads: {'fields': ['a', 'b', 'c']}
- kv: flat {str: str}
  - dumps: 'k1=v1;k2=v2'
  - loads: {'k1': 'v1', 'k2': 'v2'}
- pylit: any literal
  - dumps: repr(obj)
  - loads: ast.literal_eval(s)

Stdlib only.
"""

import csv
import io
from typing import Any, Dict, List


def dumps(obj: Any, format: str = "csv") -> str:
    """
    Serialize an object to a string based on the specified format.
    
    Args:
        obj: The object to serialize
        format: The serialization format ('csv', 'kv', or 'pylit')
    
    Returns:
        A string representation of the object
    """
    if format == "csv":
        if not isinstance(obj, dict) or "fields" not in obj:
            raise ValueError("CSV format requires an object with 'fields' key")
        
        fields = obj["fields"]
        if not isinstance(fields, list):
            raise ValueError("'fields' must be a list")
        
        # Convert each field to string and join with commas
        return ",".join(str(field) for field in fields)
    
    elif format == "kv":
        if not isinstance(obj, dict):
            raise ValueError("KV format requires a dictionary")
        
        # Convert each key-value pair to 'key=value' format and join with semicolons
        return ";".join(f"{k}={v}" for k, v in obj.items())
    
    elif format == "pylit":
        # Use repr to get a string representation of the object
        return repr(obj)
    
    else:
        raise ValueError(f"Unknown format: {format}")


def loads(s: str, format: str = "csv") -> Any:
    """
    Deserialize a string to an object based on the specified format.
    
    Args:
        s: The string to deserialize
        format: The deserialization format ('csv', 'kv', or 'pylit')
    
    Returns:
        The deserialized object
    """
    if format == "csv":
        # Split the string by commas and create a list of fields
        fields = [field.strip() for field in s.split(",")]
        return {"fields": fields}
    
    elif format == "kv":
        result = {}
        # Split by semicolons and parse each key=value pair
        for pair in s.split(";"):
            if "=" in pair:
                key, value = pair.split("=", 1)
                result[key.strip()] = value.strip()
        return result
    
    elif format == "pylit":
        import ast
        # Use ast.literal_eval for safe evaluation
        return ast.literal_eval(s)
    
    else:
        raise ValueError(f"Unknown format: {format}")
