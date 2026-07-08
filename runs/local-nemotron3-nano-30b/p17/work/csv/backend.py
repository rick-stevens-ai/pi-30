def dumps(obj):
    """Serialize {'fields': [...]} dict to CSV format 'a,b,c'."""
    return ','.join(obj["fields"])


def loads(s):
    """Deserialize CSV format back to {'fields': [...]} dict."""
    if not s:
        fields = []
    else:
        fields = s.split(',')
    return {"fields": fields}