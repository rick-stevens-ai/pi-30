"""
CSV backend - simple serialization of list of fields.

The backend exposes the following API used by the tests:

    dumps(obj) -> str
    loads(s)   -> obj

Where `obj` is a dict of the form ``{"fields": [...]}``.  The list may contain
strings, numbers, or any JSON-serialisable type but the tests use only plain
strings.

Implementation uses the stdlib :mod:`csv` module to correctly escape commas,
quotes, newlines etc.  The writer is configured for minimal output by using
``csv.QUOTE_MINIMAL``.
"""

import csv
from io import StringIO

__all__ = ["dumps", "loads"]


def dumps(obj: dict) -> str:
    """Serialize ``obj`` into a comma-separated string.

    Parameters
    ----------
    obj:
        Dictionary with a single key ``"fields"`` pointing to an iterable of
        values.

    Returns
    -------
    str:
        The CSV representation of the fields.

    Examples
    --------
    >>> dumps({"fields": ["a", "b", "c"]})
    'a,b,c'

    Notes
    -----
    The function uses :class:`csv.writer` to handle quoting rules.  It writes a
    single row and returns the underlying string.
    """
    if not isinstance(obj, dict) or "fields" not in obj:
        raise TypeError("obj must be a dict containing the key 'fields'")
    fields = obj["fields"]
    output = StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(fields)
    return output.getvalue().rstrip("\n")


def loads(s: str) -> dict:
    """Deserialize a CSV string into ``obj``.

    Parameters
    ----------
    s:
        CSV-encoded string.

    Returns
    -------
    dict:
        ``{"fields": [list_of_values]}``.

    The function tolerates an empty string and returns an empty list.
    """
    if s == "":
        return {"fields": []}
    input_io = StringIO(s)
    reader = csv.reader(input_io)
    rows = list(reader)
    if not rows:
        return {"fields": []}
    # Only the first row is considered.
    return {"fields": rows[0]}

"""End of csv backend."""
