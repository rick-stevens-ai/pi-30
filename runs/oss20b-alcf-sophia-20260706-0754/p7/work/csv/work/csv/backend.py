import csv
from typing import Dict, List


def parse(text: str) -> Dict[str, List[str]]:
    """Parse a single CSV line.

    The expected input is a simple comma‑separated line such as
    ``"a,b,c"``.

    ``csv`` from the standard library handles the common CSV edge cases
    (quoted fields, escaped commas, etc.).  The output is a dictionary
    with a single key ``"fields"`` mapping to the list of values.

    Parameters
    ----------
    text:
        The CSV line to parse.

    Returns
    -------
    dict
        ``{"fields": [<field1>, <field2>, ...]}``
    """

    # ``csv.reader`` expects an iterable of lines.  A simple list with the
    # single input string is sufficient.  ``strip`` removes any stray newline
    # that might otherwise become an empty field.
    reader = csv.reader([text.strip()])
    try:
        row = next(reader)
    except StopIteration:
        row = []
    return {"fields": row}
