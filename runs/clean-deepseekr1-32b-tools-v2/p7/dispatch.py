def dispatch(kind, text):
    if kind == 'csv':
        from work.csv.backend import parse
        return parse(text)
    elif kind == 'kv':
        from work.kv.backend import parse
        return parse(text)
    elif kind == 'json':
        from work.json.backend import parse
        return parse(text)