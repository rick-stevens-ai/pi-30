def fmt(d: dict) -> str:
    """Formats a dictionary as a single line 'k=v k=v ...' with keys ALPHA-sorted."""
    return " ".join(f"{k}={v}" for k, v in sorted(d.items()))
