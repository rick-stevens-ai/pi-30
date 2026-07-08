def fmt(d):
    """Format a dict as 'k=v k=v ...' with keys ALPHA-sorted."""
    return " ".join(f"{k}={v}" for k, v in sorted(d.items()))
