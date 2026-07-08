def agg(nums: list[float]) -> dict:
    """
    Aggregates a list of numbers to calculate count, sum, mean, min, and max.
    """
    if not nums:
        return {"count": 0, "sum": 0.0, "mean": 0.0, "min": float('inf'), "max": float('-inf')}

    count = len(nums)
    total_sum = sum(nums)
    mean = total_sum / count
    minimum = min(nums)
    maximum = max(nums)

    return {
        "count": count,
        "sum": total_sum,
        "mean": mean,
        "min": minimum,
        "max": maximum
    }

if __name__ == '__main__':
    # Example usage (assuming clean stage output)
    test_data = [1.0, 2.5, 3.0, 4.5, 5.0]
    result = agg(test_data)
    print(f"Input: {test_data}")
    print(f"Result: {result}")

    empty_data = []
    result_empty = agg(empty_data)
    print(f"Input: {empty_data}")
    print(f"Result: {result_empty}")