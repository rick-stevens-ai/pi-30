def parse(text: str) -> dict:
    result = {}
    for pair in text.split(";"):
        if not pair:
            continue
        k, _, v = pair.partition("=")
        result[k] = v
    return result
