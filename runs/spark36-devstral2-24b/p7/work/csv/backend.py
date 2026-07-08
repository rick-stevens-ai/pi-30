"""
CSV parser backend for P7.
Exposes parse(text: str) -> dict
"""

def parse(text: str) -> dict:
    """
    Parse a single CSV line into a dict with fields list.
    Example: 'a,b,c' -> {'fields': ['a', 'b', 'c']}
    """
    if not text:
        return {"fields": []}
    
    fields = [f.strip() for f in text.split(',')]
    return {"fields": fields}
