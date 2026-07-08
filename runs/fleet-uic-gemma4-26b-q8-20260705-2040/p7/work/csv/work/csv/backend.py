import csv
import io

def parse(text: str) -> dict:
    """
    Parses a single CSV line into a dictionary with a 'fields' key.
    Example: "a,b,c" -> {"fields": ["a", "b", "c"]}
    """
    if not text:
        return {"fields": []}
    reader = csv.reader(io.StringIO(text))
    try:
        row = next(reader)
        return {"fields": row}
    except StopIteration:
        return {"fields": []}
