def parse(text):
    result = {}
    for pair in text.split(";"):
        if pair:
            k, v = pair.split("=", 1)
            result[k] = v
    return result
