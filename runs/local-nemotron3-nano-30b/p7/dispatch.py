def dispatch(kind, text):
    """
    Dispatch `text` to the appropriate backend based on `kind`.
    Supported kinds: "csv", "kv", "json".
    
    The function imports and calls `parse(text)` from the corresponding
    backend module located at work/{csv,kv,json}/backend.py.
    Returns a dict result of that parser.
    """
    if kind == "csv":
        # Import lazily to avoid circular dependencies if needed
        from work.csv.backend import parse as csv_parse
        return csv_parse(text)
    elif kind == "kv":
        from work.kv.backend import parse as kv_parse
        return kv_parse(text)
    elif kind == "json":
        from work.json.backend import parse as json_parse
        return json_parse(text)
    else:
        raise ValueError(f"Unsupported kind: {kind!r}")