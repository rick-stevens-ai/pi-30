"""Stage functions for data pipeline: clean, agg, fmt."""

from typing import Any


def clean(rows: list[Any]) -> list[float]:
    """Drop any element not convertible to float (None, '', 'x' dropped)."""
    result = []
    for row in rows:
        try:
            result.append(float(row))
        except (TypeError, ValueError):
            pass
    return result


def agg(nums: list[float]) -> dict[str, float | int]:
    """Aggregate numbers into count, sum, mean, min, max."""
    if not nums:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}
    count = len(nums)
    total = sum(nums)
    return {
        "count": count,
        "sum": float(total),
        "mean": float(total) / count,
        "min": min(nums),
        "max": max(nums),
    }


def fmt(d: dict[str, float | int]) -> str:
    """Format dict as single line 'k=v k=v ...' with keys ALPHA-sorted."""
    parts = [f"{k}={d[k]}" for k in sorted(d.keys())]
    return " ".join(parts)
