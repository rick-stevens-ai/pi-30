"""
KV backend serializer.
Obj is a flat {str:str} dict.
dumps -> "k1=v1;k2=v2", loads -> {}
"""
from typing import Dict


def dumps(obj: Dict[str, str]) -> str:
    """
    Serialize a flat dictionary to key=value pairs joined by semicolons.
    
    Args:
        obj: A dictionary with string keys and values
        
    Returns:
        A string in format "k1=v1;k2=v2;..."
    """
    return ";".join(f"{k}={v}" for k, v in sorted(obj.items()))


def loads(s: str) -> Dict[str, str]:
    """
    Deserialize a key=value string back to a dictionary.
    
    Args:
        s: A string in format "k1=v1;k2=v2;..."
        
    Returns:
        A flat dictionary with string keys and values
    """
    result = {}
    if not s:
        return result
    
    for pair in s.split(";"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            result[key] = value
    
    return result
