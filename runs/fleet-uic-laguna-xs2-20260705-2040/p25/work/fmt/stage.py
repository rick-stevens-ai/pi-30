def fmt(d):
    """Format dict to a single line 'k=v k=v ...' with keys ALPHA-sorted.

    Args:
        d: Dict with string keys and values

    Returns:
        str: Single line formatted string with alpha-sorted keys
    """
    sorted_keys = sorted(d.keys())
    return " ".join(f"{k}={d[k]}" for k in sorted_keys)