"""CSV backend: parse a single CSV line -> {'fields': [...]}"""


def parse(text: str) -> dict:
    """Parse a single CSV line and return a dict with 'fields' key.
    
    Args:
        text: A CSV line string like "a,b,c"
        
    Returns:
        A dict like {"fields": ["a", "b", "c"]}
    """
    if not text:
        return {"fields": []}
    return {"fields": text.split(",")}