"""csv backend.

Shared interface:
    parse(text: str) -> dict

Parses a single CSV line "a,b,c" -> {"fields": ["a", "b", "c"]}.
Uses the stdlib csv module so quoted fields are handled correctly.
"""

import csv
import io


def parse(text: str) -> dict:
    reader = csv.reader(io.StringIO(text))
    fields = next(reader)
    return {"fields": fields}