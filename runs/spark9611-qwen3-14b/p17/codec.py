import importlib

def round_trip(fmt, obj):
    module_path = f"work.{fmt}.backend"
    backend = importlib.import_module(module_path)
    s = backend.dumps(obj)
    return backend.loads(s)