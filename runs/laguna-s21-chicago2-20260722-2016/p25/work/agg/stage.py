"""agg stage: aggregate a list of floats into summary statistics.

agg(nums) -> {"count":int, "sum":float, "mean":float, "min":float, "max":float}
"""

import math


def agg(nums):
    """Aggregate numeric values into count/sum/mean/min/max.

    Uses math.fsum for the running sum to avoid floating-point drift in
    large inputs (stdlib only).  An empty input yields zeroed stats so the
    downstream fmt stage always receives well-typed floats.
    """
    n = len(nums)
    if n == 0:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}
    total = math.fsum(nums)
    return {
        "count": n,
        "sum": float(total),
        "mean": float(total) / n,
        "min": float(min(nums)),
        "max": float(max(nums)),
    }