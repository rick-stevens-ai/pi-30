"""sort.py - Candidate #2: Iterative Bottom-Up Merge Sort with Insertion Sort for Small Runs.

This is a distinct algorithmic approach from Candidate #1's built-in Timsort:
- Iterative bottom-up merge sort (no recursion, no recursion limit issues)
- Stable sort (preserves multiset order for equal elements)
- O(n log n) worst-case time complexity, O(n) space
- Insertion sort for small runs (optimizes small arrays and nearly-sorted data)
- Pure Python implementation (no built-in sort)
- Stable sort: preserves multiset order for equal elements
"""

def _insertion_sort(arr, left, right):
    """Insertion sort for small subarrays [left, right). Stable."""
    for i in range(left + 1, right):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def _merge(arr, temp, left, mid, right):
    """Merge two sorted subarrays [left, mid) and [mid, right) into temp, then copy back. Stable."""
    i, j, k = left, mid, left
    
    # Merge with stability: use <= to preserve order of equal elements
    while i < mid and j < right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            j += 1
        k += 1
    
    # Copy remaining elements
    while i < mid:
        temp[k] = arr[i]
        i += 1
        k += 1
    while j < right:
        temp[k] = arr[j]
        j += 1
        k += 1
    
    # Copy back to original array
    for i in range(left, right):
        arr[i] = temp[i]


def _bottom_up_merge_sort(arr):
    """Iterative bottom-up merge sort with insertion sort for small runs. Stable, O(n log n)."""
    n = len(arr)
    if n < 2:
        return
    
    temp = [None] * n
    RUN_SIZE = 32  # Optimal run size for insertion sort (similar to Timsort)
    
    # Step 1: Sort small runs with insertion sort
    for start in range(0, n, RUN_SIZE):
        end = min(start + RUN_SIZE, n)
        _insertion_sort(arr, start, end)
    
    # Step 2: Merge runs bottom-up, doubling size each pass
    size = RUN_SIZE
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size, n)
            right = min(left + 2 * size, n)
            if mid < right:  # Only merge if there are two runs
                _merge(arr, temp, left, mid, right)
        size *= 2


def my_sort(xs):
    """Return a new list containing all elements of xs in ascending order.
    
    Args:
        xs: Any iterable of orderable elements.
        
    Returns:
        A new sorted list (ascending). Original input is not modified.
        Stable sort: preserves relative order of equal elements (multiset preserved).
    """
    arr = list(xs)  # Convert to list (handles any iterable, copies input)
    _bottom_up_merge_sort(arr)
    return arr


if __name__ == "__main__":
    # Quick sanity checks
    assert my_sort([]) == []
    assert my_sort([1]) == [1]
    assert my_sort([3, 1, 2]) == [1, 2, 3]
    assert my_sort([5, 5, 5]) == [5, 5, 5]
    assert my_sort([-3, -1, -2, 0]) == [-3, -2, -1, 0]
    assert my_sort([10**100, 1, 10**50]) == [1, 10**50, 10**100]
    assert my_sort([3, 1, 2, 1, 3]) == [1, 1, 2, 3, 3]  # multiset preserved
    
    # Test stability: equal elements should preserve original order
    # Using tuples (value, original_index) to verify stability
    test_stability = [(3, 0), (1, 0), (2, 0), (1, 1), (3, 1)]
    sorted_stable = my_sort(test_stability)
    assert sorted_stable == [(1, 0), (1, 1), (2, 0), (3, 0), (3, 1)], "Stability test failed"
    
    # Large array test
    import random
    large = list(range(10000))
    random.shuffle(large)
    assert my_sort(large) == list(range(10000))
    
    # Large integers
    assert my_sort([2**1000, 2**100, 2**500]) == [2**100, 2**500, 2**1000]
    
    # Already sorted
    assert my_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    
    # Reverse sorted
    assert my_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    
    print("All tests passed.")
