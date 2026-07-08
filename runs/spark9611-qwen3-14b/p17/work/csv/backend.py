def dumps(obj):
    return ",".join(obj["fields"])

def loads(s):
    return {"fields": s.split(",")}