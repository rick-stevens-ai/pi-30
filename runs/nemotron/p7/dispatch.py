"""Dispatch module: routes to the appropriate backend based on kind."""
import sys
import os

# Add work directory to path so we can import backends
work_dir = os.path.join(os.path.dirname(__file__), 'work')
sys.path.insert(0, work_dir)

# Import backends using absolute imports to avoid stdlib conflicts
from work.csvbe.backend import parse as parse_csv
from work.kvbe.backend import parse as parse_kv
from work.jsonbe.backend import parse as parse_json


def dispatch(kind: str, text: str) -> dict:
    """Dispatch to the appropriate backend based on kind."""
    if kind == "csv":
        return parse_csv(text)
    elif kind == "kv":
        return parse_kv(text)
    elif kind == "json":
        return parse_json(text)
    else:
        raise ValueError(f"Unknown kind: {kind}")
