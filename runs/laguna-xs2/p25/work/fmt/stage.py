def fmt(d):
    """fmt(d) -> single line 'k=v k=v ...' with keys ALPHA-sorted."""
    parts = [f"{k}={v}" for k, v in sorted(d.items())]
    return " ".join(parts)