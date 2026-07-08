"""CSV backend: parse a single CSV line into {"fields": [...]}.

Usage:
    from csv.backend import parse
    parse("a,b,c")  # -> {"fields": ["a", "b", "c"]}
"""

import csv


def parse(text: str) -> dict:
    """Parse a single CSV line and return ``{"fields": [<values>]} ``.

    Parameters
    ----------
    text : str
        A single CSV record, e.g. ``"a,b,c"`` or just ``"solo"``.

    Returns
    -------
    dict
        ``{"fields": [...]}`` containing the parsed field values.
    """
    reader = csv.reader([text])
    row = next(reader)
    return {"fields": row}
