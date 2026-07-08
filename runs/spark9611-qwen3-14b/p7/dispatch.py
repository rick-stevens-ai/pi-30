def dispatch(kind, text):
    if kind == 'csv':
        import work.csv.backend as backend
    elif kind == 'kv':
        import work.kv.backend as backend
    elif kind == 'json':
        import work.json.backend as backend
    else:
        raise ValueError(f"Unknown kind: {kind}")
    return backend.parse(format=text)