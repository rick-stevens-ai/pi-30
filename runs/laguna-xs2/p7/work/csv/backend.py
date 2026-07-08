# csv backend: parse a single CSV line
# parse(text: str) -> dict

def parse(text: str) -> dict:
    """Parse a single CSV line 'a,b,c' -> {'fields': ['a','b','c']}"""
    if text is None:
        return {'fields': []}
    fields = text.split(',')
    return {'fields': fields}