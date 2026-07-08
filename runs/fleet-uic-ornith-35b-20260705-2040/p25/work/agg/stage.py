"""Aggregate statistics over a list of numbers."""


def agg(nums: "list[float]") -> "dict[str, float | int]":
    """Return count, sum, mean, min, max for *nums*."""
    if not nums:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}

    total = float(sum(nums))
    n = len(nums)
    return {
        "count": n,
        "sum": total,
        "mean": total / n,
        "min": float(min(nums)),
        "max": float(max(nums)),
    }
