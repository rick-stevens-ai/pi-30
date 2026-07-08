def my_sort(xs):
    """
    Sort the input list in ascending order.
    Returns a new sorted list, preserving the multiset of elements.
    Handles all edge cases: empty lists, singletons, duplicates, negatives, and large integers.
    Uses a fast algorithm suitable for large arrays.
    """
    if len(xs) <= 1:
        return xs.copy() if xs else []
    
    # Use Timsort (Python's built-in sort) for optimal performance
    # Timsort is a hybrid stable sorting algorithm derived from merge sort and insertion sort
    # It has O(n log n) complexity in the worst case and is highly optimized for real-world data
    sorted_list = sorted(xs)
    return sorted_list


if __name__ == "__main__":
    # Test cases
    test_cases = [
        [],  # Empty list
        [1],  # Singleton
        [1, 1, 1],  # All duplicates
        [3, 1, 2],  # Unsorted with duplicates
        [-5, -1, -3],  # Negative numbers
        [10**18, -10**18, 0],  # Large integers
        [5, 3, 1, 4, 2],  # Larger unsorted list
        list(range(1000, 0, -1)),  # Reverse sorted large list
    ]
    
    for test in test_cases:
        result = my_sort(test)
        print(f"Input: {test}")
        print(f"Output: {result}")
        print(f"Is sorted: {result == sorted(test)}")
        print(f"Multiset preserved: {sorted(test) == sorted(result)}")
        print()
