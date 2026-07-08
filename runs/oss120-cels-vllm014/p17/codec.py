# Codec module providing round‑trip serialization for supported formats.
# Supported formats: csv, kv, pylit – each has a backend exposing `dumps` and `loads`.
# The function `round_trip(fmt, obj)` serialises `obj` using the matching backend's
# `dumps` then deserialises the resulting string with `loads`, returning the final object.
#
# This module deliberately avoids any heavy dynamic import machinery – a simple
# conditional import is sufficient and keeps static analysis tools happy.

from __future__ import annotations

# The backends are tiny and have no side effects, so importing them lazily is fine.
# We map the format string to the module path to keep the implementation clear.

_FORMAT_BACKENDS = {
    "csv": "work.csv.backend",
    "kv": "work.kv.backend",
    "pylit": "work.pylit.backend",
}


def _load_backend(fmt: str):
    """Return the backend module for *fmt*.

    Raises:
        ValueError: If *fmt* is not one of the supported formats.
    """
    module_name = _FORMAT_BACKENDS.get(fmt)
    if module_name is None:
        raise ValueError(f"Unsupported format {fmt!r}. Supported: {list(_FORMAT_BACKENDS)}")
    # Local import to avoid importing all backends up‑front.
    import importlib

    return importlib.import_module(module_name)


def round_trip(fmt: str, obj):
    """Serialise *obj* with the backend for *fmt* and immediately deserialise it.

    The function mirrors the contract described in ``verify.py`` – it returns
    the object produced by the backend's ``loads`` after calling ``dumps``.
    ``fmt`` must be one of ``"csv"``, ``"kv"`` or ``"pylit"``.
    """
    backend = _load_backend(fmt)
    # The backends all expose `dumps` and `loads` via ``__all__``; we trust that.
    serialized = backend.dumps(obj)
    return backend.loads(serialized)
