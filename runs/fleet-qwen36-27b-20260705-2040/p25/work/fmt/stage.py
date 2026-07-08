def fmt(d):
    """Format a dict as 'k=v k=v ...' with keys alpha-sorted."""
    return ' '.join(f'{k}={d[k]}' for k in sorted(d))
