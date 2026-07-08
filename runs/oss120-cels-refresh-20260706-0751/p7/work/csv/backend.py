"""CSV backend parser.

Provides a single function `parse` that converts a CSV line string into a
dictionary with a single key ``fields`` mapping to a list of the individual
field values.

The implementation is deliberately minimal – it does not handle quoted
fields, escaped commas, or any of the richer CSV semantics because the
specification for this exercise only requires splitting a simple line such
as ``"a,b,c"`` into ``{"fields": ["a", "b", "c"]}``.

If the input string is empty the function returns an empty list of fields.
"""

from __future__ import annotations


def parse(text: str) -> dict:
    """Parse a single CSV line.

    The parser treats the input as a plain, comma‑separated list of values.
    No quoting or escaping is performed – each comma simply delineates a
    field. Whitespace characters are preserved as‑is.

    Parameters
    ----------
    text: str
        The CSV line to parse.

    Returns
    -------
    dict
        ``{"fields": [...]}`` where the list contains the split field values.
    """
    # Split on commas; an empty string should yield an empty list.
    if text == "":
        fields: list[str] = []
    else:
        fields = text.split(",")
    return {"fields": fields}
