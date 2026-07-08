from work.kv.backend import parse as _parse_kv


def dispatch(kind, text):
    """Dispatch to the appropriate backend parser based on kind."""
    if kind == "kv":
        return _parse_kv(text)
