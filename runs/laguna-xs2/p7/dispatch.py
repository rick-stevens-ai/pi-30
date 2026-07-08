# Dispatch module: route parsing to appropriate backend

from work.csv.backend import parse as csv_parse
from work.kv.backend import parse as kv_parse
from work.json.backend import parse as json_parse


def dispatch(kind: str, text: str) -> dict:
    """Route parsing to the appropriate backend based on kind.
    
    Args:
        kind: One of 'csv', 'kv', 'json'
        text: The text to parse
        
    Returns:
        The parsed dictionary
    """
    if kind == "csv":
        return csv_parse(text)
    elif kind == "kv":
        return kv_parse(text)
    elif kind == "json":
        return json_parse(text)
    else:
        raise ValueError(f"Unknown kind: {kind}")