def fmt(d: dict) -> str:
    """
    Formats a dictionary into a single line 'k=v k=v ...' with keys ALPHA-sorted.
    """
    sorted_keys = sorted(d.keys())
    parts = [f"{k}={d[k]}" for k in sorted_keys]
    return " ".join(parts)
