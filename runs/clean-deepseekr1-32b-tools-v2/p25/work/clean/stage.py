def clean(rows):
    cleaned = []
    for item in rows:
        try:
            if isinstance(item, (str, bytes)) and not item.strip():
                continue
            num = float(item)
            cleaned.append(num)
        except (ValueError, TypeError):
            pass
    return cleaned