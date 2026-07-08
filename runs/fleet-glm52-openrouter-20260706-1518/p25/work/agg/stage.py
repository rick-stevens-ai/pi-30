"""agg stage: aggregate a list of floats into summary statistics."""


def agg(nums):
    """agg(nums) -> {'count':int,'sum':float,'mean':float,'min':float,'max':float}.

    Computes summary statistics over a list of numbers. Returns a dict with
    count, sum, mean, min, max. For an empty input, count is 0 and the other
    fields default to 0.0 (no division by zero).
    """
    nums = list(nums)
    count = len(nums)
    if count == 0:
        return {
            "count": 0,
            "sum": 0.0,
            "mean": 0.0,
            "min": 0.0,
            "max": 0.0,
        }
    total = float(sum(nums))
    mean = total / count
    return {
        "count": count,
        "sum": total,
        "mean": mean,
        "min": float(min(nums)),
        "max": float(max(nums)),
    }
