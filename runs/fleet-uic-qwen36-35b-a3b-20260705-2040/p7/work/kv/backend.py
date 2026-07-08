def parse(text: str) -> dict:
    result = {}
    for pair in text.split(";"):
        if not pair.strip():
            continue
        key, value = pair.split("=", 1)
        result[key] = value
    return result
