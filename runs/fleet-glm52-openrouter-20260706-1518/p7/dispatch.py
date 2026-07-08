"""Dispatch parser front-end routing kind in {csv,kv,json} to backend.parse."""

from work.csv.backend import parse as parse_csv
from work.kv.backend import parse as parse_kv
from work.json.backend import parse as parse_json

_BACKENDS = {
    "csv": parse_csv,
    "kv": parse_kv,
    "json": parse_json,
}


def dispatch(kind: str, text: str) -> dict:
    """Route `kind` to the matching backend parser and return its dict."""
    try:
        backend = _BACKENDS[kind]
    except KeyError:
        raise ValueError(f"unknown parser kind: {kind!r}")
    return backend(text)
