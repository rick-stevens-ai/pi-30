"""CSV backend: parse a single CSV line 'a,b,c' -> {'fields': ['a','b','c']}."""
import csv
import io


def parse(text: str) -> dict:
    """Parse a single CSV line to {'fields': [...]}."""
    if not text:
        return {"fields": []}
    f = io.StringIO(text)
    reader = csv.reader(f)
    row = next(reader, [])
    return {"fields": row}
