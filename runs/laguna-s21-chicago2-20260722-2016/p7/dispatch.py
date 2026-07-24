"""Dispatcher wiring the three backend parsers to a single entry point.

Each backend lives in work/<kind>/backend.py and exposes:
    parse(text: str) -> dict

This module exposes:
    dispatch(kind: str, text: str) -> dict
routing ``kind`` in {"csv", "kv", "json"} to the matching backend.
"""

import importlib

_BACKENDS = ("csv", "kv", "json")


def _get_backend(kind):
    """Return the backend module for ``kind``, raising on unknown kinds."""
    if kind not in _BACKENDS:
        raise ValueError(
            "unknown backend kind %r; expected one of %s"
            % (kind, ", ".join(_BACKENDS))
        )
    return importlib.import_module("work.%s.backend" % kind)


def dispatch(kind: str, text: str) -> dict:
    """Parse ``text`` using the backend identified by ``kind``.

    Args:
        kind: One of "csv", "kv", "json".
        text: The raw text to parse.

    Returns:
        The dict produced by the matching backend's ``parse`` function.

    Raises:
        ValueError: If ``kind`` is not a supported backend.
    """
    return _get_backend(kind).parse(text)


if __name__ == "__main__":
    # Tiny smoke test when run directly.
    print(dispatch("csv", "a,b,c"))
    print(dispatch("kv", "k1=v1;k2=v2"))
    print(dispatch("json", '{"x": 1, "y": [2, 3]}'))