import importlib


def round_trip(fmt: str, obj) -> object:
    backend = importlib.import_module(f"work.{fmt}.backend")
    return backend.loads(backend.dumps(obj))
