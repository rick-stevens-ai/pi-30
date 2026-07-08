"""Dispatch module for routing text parsing to appropriate backend."""

from work.csv.backend import parse as parse_csv
from work.kv.backend import parse as parse_kv
from work.json.backend import parse as parse_json


def dispatch(kind: str, text: str) -> dict:
    """Dispatch text parsing to the appropriate backend based on kind.
    
    Args:
        kind: One of 'csv', 'kv', or 'json'
        text: The text to parse
        
    Returns:
        Parsed dictionary
        
    Raises:
        ValueError: If kind is not one of the supported formats
    """
    if kind == 'csv':
        return parse_csv(text)
    elif kind == 'kv':
        return parse_kv(text)
    elif kind == 'json':
        return parse_json(text)
    else:
        raise ValueError(f"Unsupported kind: {kind}")
