def fmt(d):
    """Return single line 'k=v k=v ...' with keys alpha-sorted."""
    parts = [f"{k}={v}" for k, v in sorted(d.items())]
    return " ".join(parts)
