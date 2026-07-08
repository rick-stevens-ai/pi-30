def fmt(d):
    """
    Formats a dictionary into a single line string 'k=v k=v ...' 
    with keys sorted alphabetically.
    """
    sorted_keys = sorted(d.keys())
    return " ".join(f"{k}={d[k]}" for k in sorted_keys)
