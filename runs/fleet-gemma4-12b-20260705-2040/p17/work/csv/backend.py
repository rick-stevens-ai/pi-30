def dumps(obj):
    return ",".join(map(str, obj["fields"]))

def loads(s):
    if s == "":
        return {"fields": []}
    return {"fields": s.split(",")}
