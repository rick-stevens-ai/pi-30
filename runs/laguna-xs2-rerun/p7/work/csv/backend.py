"""CSV backend: parse 'a,b,c' -> {'fields': ['a', 'b', 'c']}"""


def parse(text: str) -> dict:
    """Parse a CSV line into a dict with 'fields' key."""
    if not text:
        return {"fields": []}
    return {"fields": text.split(',')}