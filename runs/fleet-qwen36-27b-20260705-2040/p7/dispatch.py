"""Dispatch text to the appropriate backend parser by kind."""

from work.csv.backend import parse as csv_parse
from work.kv.backend import parse as kv_parse
from work.json.backend import parse as json_parse

_BACKENDS = {
    "csv": csv_parse,
    "kv": kv_parse,
    "json": json_parse,
}


def dispatch(kind: str, text: str) -> dict:
    """Route *text* to the parser identified by *kind* and return the result."""
    try:
        return _BACKENDS[kind](text)
    except KeyError:
        raise ValueError(f"Unknown kind: {kind!r}")
