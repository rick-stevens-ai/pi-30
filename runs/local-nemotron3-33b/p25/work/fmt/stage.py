def fmt(d):
    """Format dict of stats as 'key=value' strings sorted alphabetically by key.""" 
    parts = []
    for k in sorted(d.keys()):
        v = d[k]
        if isinstance(v, float) and v.is_integer():
            val_str = str(int(v))
        else:
            val_str = str(v)
        parts.append(f"{k}={val_str}")
    return " ".join(parts)