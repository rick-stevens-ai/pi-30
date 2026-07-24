import importlib

def round_trip(fmt, obj):
    backend = importlib.import_module(f"work.{fmt}.backend")
    return backend.loads(backend.dumps(obj))
