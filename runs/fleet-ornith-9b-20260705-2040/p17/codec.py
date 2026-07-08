# codec.py: round_trip(fmt, obj) -> loads(dumps(obj)) using work/<fmt>/backend.py

def _import_backend(fmt):
    mod = __import__(f"work.{fmt}.backend", fromlist=["dumps", "loads"])
    # pylit backend exposes a two-arg registry API (dumps(fmt, obj), loads(fmt, s)).
    # csv and kv expose one-arg standalone functions. Use the right signature.
    if mod.dumps.__code__.co_argcount == 2:
        dumps_fn = lambda obj: mod.dumps(fmt, obj)
        loads_fn = lambda s: mod.loads(fmt, s)
    else:
        dumps_fn = mod.dumps
        loads_fn = mod.loads
    return dumps_fn, loads_fn


def round_trip(fmt, obj):
    dumps_fn, loads_fn = _import_backend(fmt)
    s = dumps_fn(obj)
    return loads_fn(s)
