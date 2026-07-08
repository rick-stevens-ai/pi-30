"""
Codec module that provides round_trip functionality using different backends.
"""
from typing import Any

def round_trip(fmt: str, obj: Any) -> Any:
    """
    Perform a round trip serialization/deserialization using the specified format.
    
    Args:
        fmt: Format name ('csv', 'kv', or 'pylit')
        obj: Object to serialize
        
    Returns:
        Deserialized object after round trip
    """
    # Import the appropriate backend module
    if fmt == 'csv':
        from work.csv.backend import dumps, loads
    elif fmt == 'kv':
        from work.kv.backend import dumps, loads
    elif fmt == 'pylit':
        from work.pylit.backend import dumps, loads
    else:
        raise ValueError(f"Unknown format: {fmt}")
    
    # Perform the round trip
    return loads(dumps(obj))
