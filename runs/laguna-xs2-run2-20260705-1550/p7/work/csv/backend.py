"""CSV backend: parse a single CSV line -> dict with 'fields' key."""

import csv
from io import StringIO


def parse(text: str) -> dict:
    """Parse a single CSV line and return dict with 'fields' key.
    
    Args:
        text: A single CSV line string like "a,b,c"
        
    Returns:
        dict with 'fields' key containing list of field values
    """
    reader = csv.reader(StringIO(text))
    try:
        fields = next(reader)
    except StopIteration:
        fields = []
    return {"fields": fields}