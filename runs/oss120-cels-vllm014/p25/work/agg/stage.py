"""agg stage implementation.

According to the plan, this stage receives a list of numbers (floats) and should
return a dictionary containing basic statistics: count, sum, mean, min, and max.
All values are numeric types (int for count, float for the others).

Only the Python standard library is used.
"""

def agg(nums):
    """Aggregate a list of numbers into basic statistics.

    Args:
        nums (list[float]): List of numeric values.

    Returns:
        dict: Mapping with keys 'count', 'sum', 'mean', 'min', 'max'.
    """
    count = len(nums)
    total = sum(nums) if count else 0.0
    # Avoid division by zero; mean is 0.0 for empty input.
    mean = total / count if count else 0.0
    # For empty input, define min and max as 0.0 (consistent numeric type).
    minimum = min(nums) if count else 0.0
    maximum = max(nums) if count else 0.0
    return {
        "count": count,
        "sum": total,
        "mean": mean,
        "min": minimum,
        "max": maximum,
    }

__all__ = ["agg"]
