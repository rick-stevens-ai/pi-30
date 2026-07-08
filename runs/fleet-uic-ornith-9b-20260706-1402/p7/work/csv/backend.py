def parse(text: str) -> dict:
    """Parse a single CSV line like 'a,b,c' into {'fields': ['a','b','c']}."""
    return {"fields": text.split(",")}
