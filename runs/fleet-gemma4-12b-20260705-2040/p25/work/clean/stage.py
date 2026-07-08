def clean(rows):
    cleaned = []
    for row in rows:
        try:
            cleaned.append(float(row))
        except (ValueError, TypeError):
            continue
    return cleaned
