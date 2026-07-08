import importlib

def round_trip(fmt: str, obj):
    module = importlib.import_module(f"work.{fmt}.backend")
    return module.loads(module.dumps(obj))
