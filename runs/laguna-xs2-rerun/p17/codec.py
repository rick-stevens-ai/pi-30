"""Integrator codec that uses the matching backend."""

import sys
import os
import importlib.util


def _load_backend(fmt):
    """Load backend module from work/<fmt>/backend.py"""
    backend_path = os.path.join(os.path.dirname(__file__), 'work', fmt, 'backend.py')
    spec = importlib.util.spec_from_file_location(fmt, backend_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def round_trip(fmt, obj):
    """Round-trip using the matching backend: loads(dumps(obj))."""
    backend = _load_backend(fmt)
    return backend.loads(backend.dumps(obj))


if __name__ == "__main__":
    from verify import main
    main()