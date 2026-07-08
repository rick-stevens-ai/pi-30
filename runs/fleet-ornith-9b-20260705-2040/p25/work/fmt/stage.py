def agg(nums):
    """Aggregate a list of numbers into count/sum/mean/min/max dict."""
    if not nums:
        return {'count': 0, 'sum': 0.0, 'mean': 0.0, 'min': 0.0, 'max': 0.0}
    c = len(nums)
    s = sum(nums)
    mn = min(nums)
    mx = max(nums)
    return {
        'count': c,
        'sum': s,
        'mean': s / c,
        'min': mn,
        'max': mx,
    }


def fmt(d):
    """Format a dict as a single line 'k=v k=v ...' with keys ALPHA-sorted."""
    return " ".join(f"{k}={v}" for k, v in sorted(d.items()))
