def fmt(d):
    """Format dict as single line 'k=v k=v ...' with keys ALPHA-sorted."""
    return ' '.join(f'{k}={d[k]}' for k in sorted(d))