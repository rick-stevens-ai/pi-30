def parse(text):
    result = {}
    for item in text.split(";"):
        if "=" in item:
            k, v = item.split("=", 1)
            result[k.strip()] = v.strip()
    return result
