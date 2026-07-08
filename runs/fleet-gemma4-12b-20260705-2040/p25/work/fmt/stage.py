def fmt(d):
    # d is a dict with keys "count", "sum", "mean", "min", "max"
    # Return a single line "k=v k=v ..." with keys ALPHA-sorted
    items = []
    for k in sorted(d.keys()):
        items.append(f"{k}={d[k]}")
    return " ".join(items)
