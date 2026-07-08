from stage import agg

def test_agg():
    test_cases = [
        ([1, 2, 3], {"count": 3, "sum": 6.0, "mean": 2.0, "min": 1.0, "max": 3.0}),
        ([], {"count": 0, "sum": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}),
        ([5.5], {"count": 1, "sum": 5.5, "mean": 5.5, "min": 5.5, "max": 5.5}),
    ]

    for nums, expected in test_cases:
        result = agg(nums)
        assert result == expected, f"Failed for {nums}: expected {expected}, got {result}"
    print("All tests passed!")

if __name__ == "__main__":
    test_agg()
