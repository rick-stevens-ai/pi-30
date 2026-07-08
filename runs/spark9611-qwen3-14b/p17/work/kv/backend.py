def dumps(obj):
    return ";".join(f"{k}={v}" for k, v in obj.items())

def loads(s):
    return {k: v for part in s.split(";") if part for k, v in [part.split("=", 1)]}