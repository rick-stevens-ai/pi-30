# agg stage: produce statistics summary

def agg(nums):
    """Compute basic integer/float statistics over *nums*.

    Returns a dictionary with keys ``count``, ``sum``, ``mean``, ``min`` and
    ``max``.  When the list is empty ``mean`` defaults to ``0.0`` and
    ``min``/``max`` are left as ``None`` – the test suite never passes an empty
    list, but this guard makes the function robust.
    """
    n = len(nums)
    if n == 0:
        return {
            "count": 0,
            "sum": 0.0,
            "mean": 0.0,
            "min": None,
            "max": None,
        }
    s = sum(nums)
    return {
        "count": n,
        "sum": float(s),
        "mean": s / n,
        "min": min(nums),
        "max": max(nums),
    }
