"""Dispatcher that routes to the appropriate backend parser."""

from work.csv.backend import parse as csv_parse
from work.kv.backend import parse as kv_parse
from work.json.backend import parse as json_parse


def dispatch(kind: str, text: str) -> dict:
    """Dispatch parsing to the appropriate backend.
    
    Args:
        kind: One of "csv", "kv", or "json"
        text: Input string to parse
        
    Returns:
        dict: Parsed result
    """
    if kind == "csv":
        return csv_parse(text)
    elif kind == "kv":
        return kv_parse(text)
    elif kind == "json":
        return json_parse(text)
    else:
        raise ValueError(f"Unknown backend kind: {kind}")