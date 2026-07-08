
def clean(rows):
    result = []
    for v in rows:
        if v is None or (isinstance(v, str) and not v.strip()):
            continue
        try:
            result.append(float(v))
        except (ValueError, TypeError):
            pass
    return result
