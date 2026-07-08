import csv
import io

def parse(text):
    """
    Parses a CSV string and returns a dictionary with the fields.
    Example: 'a,b,c' -> {'fields': ['a', 'b', 'c']}
    """
    f = io.StringIO(text)
    reader = csv.reader(f)
    try:
        row = next(reader)
        return {"fields": row}
    except StopIteration:
        return {"fields": []}
