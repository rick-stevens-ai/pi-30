"""csv backend.

Serializes an object of the form {"fields":[...]} to a comma-separated
string and parses such a string back into the same object.

Stdlib only.
"""

from csv import reader as _csv_reader, writer as _csv_writer
from io import StringIO


def dumps(obj) -> str:
    """Serialize {"fields":[...]} -> 'a,b,c'."""
    if not isinstance(obj, dict):
        raise TypeError("csv backend expects a dict, got %r" % type(obj).__name__)
    if "fields" not in obj:
        raise ValueError("csv backend expects a 'fields' key, got %r" % (obj,))
    fields = obj["fields"]
    if not isinstance(fields, (list, tuple)):
        raise TypeError(
            "csv backend expects 'fields' to be a list, got %r" % type(fields).__name__
        )
    buf = StringIO()
    w = _csv_writer(buf)
    w.writerow([str(f) for f in fields])
    # csv.writer always appends a trailing "\r\n"; strip it for a clean 'a,b,c'.
    return buf.getvalue().rstrip("\r\n")


def loads(s: str):
    """Parse 'a,b,c' -> {"fields":[...]}.

    Values are returned as strings, matching the round-trip contract for a
    CSV field list (CSV carries no type information).
    """
    if not isinstance(s, str):
        raise TypeError("csv backend.loads expects a str, got %r" % type(s).__name__)
    if s == "":
        return {"fields": []}
    rows = list(_csv_reader([s]))
    if not rows:
        return {"fields": []}
    return {"fields": rows[0]}
