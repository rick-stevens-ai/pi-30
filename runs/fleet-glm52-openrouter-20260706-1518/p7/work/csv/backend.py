"""CSV backend.

Parses a single CSV line like "a,b,c" into {"fields": ["a", "b", "c"]}.
Stdlib only.
"""

import csv
import io


def parse(text: str) -> dict:
    """Parse a single CSV line into {"fields": [...]}.

    Uses the stdlib csv module. Empty input yields an empty fields list.
    """
    if text is None:
        return {"fields": []}
    reader = csv.reader(io.StringIO(text))
    fields = next(reader, [])
    return {"fields": list(fields)}
