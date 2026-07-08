def my_sort(xs: list) -> list:
    """
    Sorts a list of comparable elements in ascending order using the Merge Sort algorithm.

    This implementation is O(n log n) time complexity and is stable, ensuring correctness 
    for all edge cases (empty list, singletons, duplicates, negatives, large integers) 
    and preserving the multiset. It uses only standard Python features.

    Args:
        xs: The list of elements to be sorted.

    Returns:
        A new list containing the elements of xs sorted in ascending order.
    """
    n = len(xs)
    if n <= 1:
        return xs

    # Divide
    mid = n // 2
    left_half = xs[:mid]
    right_half = xs[mid:]

    # Conquer (Recursively sort the halves)
    sorted_left = my_sort(left_half)
    sorted_right = my_sort(right_half)

    # Combine (Merge)
    return _merge(sorted_left, sorted_right)

def _merge(left: list, right: list) -> list:
    """
    Merges two already sorted lists into a single sorted list.
    """
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged

if __name__ == '__main__':
    # Test cases
    print("Test Case 1: Empty list")
    print(f"Input: [], Output: {my_sort([])}") # Expected: []

    print("\nTest Case 2: Single element")
    print(f"Input: [5], Output: {my_sort([5])}") # Expected: [5]

    print("\nTest Case 3: Duplicates and Negatives")
    input_list = [5, -10, 0, 5, -10, 3]
    expected = [-10, -10, 0, 3, 5, 5]
    result = my_sort(input_list)
    print(f"Input: {input_list}, Output: {result}, Expected: {expected}")
    assert result == expected

    print("\nTest Case 4: Large array with varied types")
    import random
    large_list = [random.randint(-1000000, 1000000) for _ in range(100)]
    expected_large = sorted(large_list)
    result_large = my_sort(large_list)
    print(f"Large list sort successful: {result_large == expected_large}")

    print("\nTest Case 5: Big integers")
    big_ints = [10**18, 1, 999999999999999999]
    expected_big = [1, 10**18, 999999999999999999]
    result_big = my_sort(big_ints)
    print(f"Big int sort successful: {result_big == expected_big}")