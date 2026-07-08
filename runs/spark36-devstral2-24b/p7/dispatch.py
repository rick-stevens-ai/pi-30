"""
Dispatch parser based on kind.

Supported kinds:
- csv: comma-separated values
- kv: key-value pairs (k1=v1; k2=v2)
- json: JSON string
"""

def dispatch(kind, text):
    """
    Dispatch the given text to the appropriate parser based on kind.
    
    Args:
        kind (str): One of 'csv', 'kv', or 'json'.
        text (str): Text to parse.
    
    Returns:
        dict: Parsed result.
    """
    if kind == 'csv':
        from work.csv.backend import parse as csv_parse
        return csv_parse(text)
    elif kind == 'kv':
        from work.kv.backend import parse as kv_parse
        return kv_parse(text)
    elif kind == 'json':
        from work.json.backend import parse as json_parse
        return json_parse(text)
    else:
        raise ValueError(f"Unknown parser kind: {kind}")
