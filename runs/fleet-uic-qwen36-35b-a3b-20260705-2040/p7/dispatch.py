import importlib

_BACKENDS = {}


def _get_backend(kind):
    if kind not in _BACKENDS:
        mod = importlib.import_module(f"work.{kind}.backend")
        _BACKENDS[kind] = mod.parse
    return _BACKENDS[kind]


def dispatch(kind, text):
    return _get_backend(kind)(text)
