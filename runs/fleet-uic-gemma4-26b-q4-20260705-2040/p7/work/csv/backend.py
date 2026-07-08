import csv
import io

def parse(text: str) -> dict:
    """
    Parses a single CSV line.
    Example: 'a,b,c' -> {'fields': ['a', 'b', 'c']}
    """
    f = io.StringIO(text)
    reader = csv.reader(f)
    try:
        fields = next(reader)
        return {"fields": fields}
    except StopIteration:
        return {"fields": []}
