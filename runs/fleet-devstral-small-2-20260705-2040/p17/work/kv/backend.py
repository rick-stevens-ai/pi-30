"""
Backend implementations for different serialization formats.
"""


def kv_dumps(obj):
    """
    Serialize a flat dictionary (str: str) to a key-value string format.
    
    Example: {'k1': 'v1', 'k2': 'v2'} -> 'k1=v1;k2=v2'
    
    Args:
        obj: A dictionary with string keys and string values
        
    Returns:
        A string in the format 'k1=v1;k2=v2;...'
    """
    if not isinstance(obj, dict):
        raise ValueError("kv_dumps expects a dictionary")
    
    items = []
    for key, value in obj.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("kv format requires string keys and values")
        items.append(f"{key}={value}")
    
    return ";".join(items)


def kv_loads(s):
    """
    Deserialize a key-value string format back to a dictionary.
    
    Example: 'k1=v1;k2=v2' -> {'k1': 'v1', 'k2': 'v2'}
    
    Args:
        s: A string in the format 'k1=v1;k2=v2;...'
        
    Returns:
        A dictionary with string keys and values
    """
    if not isinstance(s, str):
        raise ValueError("kv_loads expects a string")
    
    result = {}
    if not s:
        return result
    
    pairs = s.split(";")
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"Invalid key-value pair: {pair}")
        key, value = pair.split("=", 1)
        result[key] = value
    
    return result
