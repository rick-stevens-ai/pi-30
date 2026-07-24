def clean(rows):
    result = []
    for r in rows:
        try:
            val = float(r)
            result.append(val)
        except (TypeError, ValueError):
            continue
    return result
