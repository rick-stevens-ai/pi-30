import importlib

def round_trip(fmt, obj):
    """
    Performs a round trip serialization and deserialization using the backend 
    specified by fmt.
    """
    module_path = f"work.{fmt}.backend"
    backend = importlib.import_module(module_path)
    return backend.loads(backend.dumps(obj))
