"""Dispatch: route parse requests to the matching backend."""


def dispatch(kind, text):
    """Route *text* to the parser for *kind*.

    Parameters
    ----------
    kind : str
        One of ``"csv"``, ``"kv"``, or ``"json"``.
    text : str
        The raw text to parse.

    Returns
    -------
    dict
        The parsed result from the corresponding backend.
    """
    if kind == "csv":
        from work.csv.backend import parse as _parse
        return _parse(text)
    elif kind == "kv":
        from work.kv.backend import parse as _parse
        return _parse(text)
    elif kind == "json":
        from work.json.backend import parse as _parse
        return _parse(text)
    else:
        raise ValueError(f"Unknown backend kind: {kind!r}")
