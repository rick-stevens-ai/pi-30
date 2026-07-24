def dumps(obj):
    return ";".join(f"{k}={v}" for k, v in obj.items())


def loads(s):
    result = {}
    if s == "":
        return result
    for part in s.split(";"):
        k, v = part.split("=", 1)
        result[k] = v
    return result
