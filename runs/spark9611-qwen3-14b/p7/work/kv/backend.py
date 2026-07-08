def parse(text):
    if not text:
        return {}
    pairs = text.split(';')
    result = {}
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            result[key.strip()] = value.strip()
    return result