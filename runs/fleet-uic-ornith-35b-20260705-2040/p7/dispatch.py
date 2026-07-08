"""Dispatch parser calls to the appropriate backend."""

import importlib


def dispatch(kind: str, text: str) -> dict:
    if kind not in ("csv", "kv", "json"):
        raise ValueError(f"Unknown backend: {kind!r}")

    # Each subpackage (e.g. work/csv/) has no __init__.py so it imports as an empty namespace package.
    pkg = None
    for name in [f"work.{kind}", f"work.{kind}.backend"]:
        try:
            m = importlib.import_module(name)
            if hasattr(m, "parse"):
                pkg = m
                break
        except ImportError:
            continue

    if not isinstance(getattr(pkg, "parse", None), object):
        raise RuntimeError(f"Could not find backend with parse() for {kind!r}")

    return pkg.parse(text)  # type: ignore[optional-item]
