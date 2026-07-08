import importlib

def round_trip(fmt: str, obj):
    """Performs a round-trip serialization/deserialization using the specified backend."""
    if fmt == "csv":
        module_path = "work.csv.backend"
    elif fmt == "kv":
        module_path = "work.kv.backend"
    elif fmt == "pylit":
        module_path = "work.pylit.work.pylit.backend"
    else:
        raise ValueError(f"Unknown format: {fmt}")

    backend = importlib.import_module(module_path)
    return backend.loads(backend.dumps(obj))
