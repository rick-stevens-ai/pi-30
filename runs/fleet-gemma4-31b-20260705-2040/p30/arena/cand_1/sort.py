def my_sort(xs):
    """
    Returns a new sorted list (ascending) containing all elements of xs.
    
    This implementation leverages Python's built-in Timsort via sorted(), 
    which is the most efficient, stable, and robust sorting algorithm available 
    in the standard library. It handles:
    - Empty lists: Returns []
    - Singletons: Returns a new list with one element
    - Duplicates: Preserves all occurrences (multiset)
    - Negatives & Big Ints: Correctly compared by Python's int type
    - Large arrays: O(n log n) time complexity, implemented in C for speed.
    
    Args:
        xs: An iterable of comparable elements.
        
    Returns:
        A new sorted list.
    """
    return sorted(xs)

if __name__ == "__main__":
    # Test cases to verify correctness
    test_cases = [
        ([], []),                                      # Empty
        ([1], [1]),                                   # Singleton
        ([3, 1, 2], [1, 2, 3]),                       # Basic
        ([5, 2, 9, 1, 5, 6], [1, 2, 5, 5, 6, 9]),     # Duplicates
        ([-1, -5, 0, 5, 1], [-5, -1, 0, 1, 5]),       # Negatives
        ([10**20, 10**10, 10**30], [10**10, 10**20, 10**30]), # Big Ints
        ([2, 2, 2, 2], [2, 2, 2, 2]),                 # All same
    ]

    for input_val, expected in test_cases:
        result = my_sort(input_val)
        assert result == expected, f"Failed on {input_val}: expected {expected}, got {result}"
    
    print("All basic tests passed!")

    # Large array test for performance check
    import random
    large_arr = [random.randint(-10**18, 10**18) for _ in range(100000)]
    sorted_large = my_sort(large_arr)
    assert sorted_large == sorted(large_arr), "Large array sort failed!"
    print("Large array test passed!")
