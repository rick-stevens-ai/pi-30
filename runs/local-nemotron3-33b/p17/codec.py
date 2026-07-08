def round_trip(fmt, obj):
    if fmt == "csv":
        from work.csv.backend import dumps as backend_dumps, loads as backend_loads
    elif fmt == "kv":
        from work.kv.backend import dumps as backend_dumps, loads as backend_loads
    elif fmt == "pylit":
        from work.pylit.backend import dumps as backend_dumps, loads as backend_loads
    else:
        raise ValueError(f"Unsupported format: {fmt}")
    return backend_loads(backend_dumps(obj))