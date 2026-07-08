"""CSV backend: parse a single CSV line into a dict with a 'fields' key."""


def parse(text: str) -> dict:
    """Parse 'a,b,c' -> {'fields': ['a', 'b', 'c']}."""
    return {"fields": text.split(",")}
