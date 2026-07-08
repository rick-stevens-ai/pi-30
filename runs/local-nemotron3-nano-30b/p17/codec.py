import importlib

def round_trip(fmt: str, obj):
    """Round-trip serializer for supported backends."""
    mod = importlib.import_module(f"work.{fmt}.backend")
    dumps_func = getattr(mod, "dumps")
    loads_func = getattr(mod, "loads")
    return loads_func(dumps_func(obj))