"""Dispatcher: route parsing requests to the appropriate backend."""
import importlib.util
import os


def _load_backend(name: str):
    """Load a backend module from work/<name>/backend.py"""
    path = os.path.join(os.path.dirname(__file__), 'work', name, 'backend.py')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_csv_backend = _load_backend('csv')
_kv_backend = _load_backend('kv')
_json_backend = _load_backend('json')


def dispatch(kind: str, text: str) -> dict:
    """Dispatch parsing to the appropriate backend.
    
    Args:
        kind: One of "csv", "kv", "json"
        text: The text to parse
    
    Returns:
        Parsed dictionary
    """
    if kind == "csv":
        return _csv_backend.parse(text)
    elif kind == "kv":
        return _kv_backend.parse(text)
    elif kind == "json":
        return _json_backend.parse(text)
    else:
        raise ValueError(f"Unknown kind: {kind}")