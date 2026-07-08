"""sort.py - Candidate #1: Use Python's built-in Timsort via sorted().

This is the optimal approach for "stdlib only + fast on large arrays + correct on all edge cases".
Timsort is:
- O(n log n) worst-case, O(n) on partially sorted data
- Stable (preserves order of equal elements → preserves multiset)
- Highly optimized C implementation
- Handles all edge cases: empty, singletons, duplicates, negatives, big ints
"""

def my_sort(xs):
    """Return a new list containing all elements of xs in ascending order.

    Args:
        xs: Any iterable of orderable elements.

    Returns:
        A new sorted list (ascending). Original input is not modified.
    """
    return sorted(xs)


if __name__ == "__main__":
    # Quick sanity checks
    assert my_sort([]) == []
    assert my_sort([1]) == [1]
    assert my_sort([3, 1, 2]) == [1, 2, 3]
    assert my_sort([5, 5, 5]) == [5, 5, 5]
    assert my_sort([-3, -1, -2, 0]) == [-3, -2, -1, 0]
    assert my_sort([10**100, 1, 10**50]) == [1, 10**50, 10**100]
    assert my_sort([3, 1, 2, 1, 3]) == [1, 1, 2, 3, 3]  # multiset preserved
    print("All basic tests passed.")