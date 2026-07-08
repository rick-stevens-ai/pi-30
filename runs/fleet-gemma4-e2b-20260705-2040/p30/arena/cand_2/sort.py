def my_sort(xs: list) -> list:
    """
    Sorts a list of comparable elements in ascending order using the Merge Sort algorithm.

    This implementation is stable, has an O(n log n) time complexity, 
    and correctly handles all edge cases (empty list, singletons, negatives, 
    duplicates, and large integers) while preserving the multiset.
    It uses only standard Python features.

    Args:
        xs: The list of elements to be sorted.

    Returns:
        A new list containing the elements of xs sorted in ascending order.
    """
    n = len(xs)
    if n <= 1:
        return xs

    # Divide the list into two halves
    mid = n // 2
    left_half = xs[:mid]
    right_half = xs[mid:]

    # Recursively sort the halves
    left = my_sort(left_half)
    right = my_sort(right_half)

    # Merge the sorted halves
    return _merge(left, right)

def _merge(left: list, right: list) -> list:
    """
    Merges two already sorted lists into a single sorted list.
    """
    merged = []
    i = 0  # Pointer for left list
    j = 0  # Pointer for right list

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
    # Test case 1: Empty list
    print(f"Test 1 (Empty): {my_sort([])}")  # Expected: []

    # Test case 2: Single element
    print(f"Test 2 (Singleton): {my_sort([42])}")  # Expected: [42]

    # Test case 3: Duplicates and negatives
    test_list_3 = [5, -1, 0, 5, -10, 3]
    print(f"Test 3 (Mixed): {my_sort(test_list_3)}") # Expected: [-10, -1, 0, 3, 5, 5]

    # Test case 4: Large numbers and mixed types (if comparable)
    import sys
    large_num = 10**18
    test_list_4 = [large_num, 1, -large_num, 0, large_num, 3.14]
    print(f"Test 4 (Large/Float): {my_sort(test_list_4)}") # Expected: [-large_num, 0, 1, 3.14, large_num, large_num]

    # Test case 5: Already sorted
    test_list_5 = [1, 2, 3, 4, 5]
    print(f"Test 5 (Sorted): {my_sort(test_list_5)}") # Expected: [1, 2, 3, 4, 5]

    # Test case 6: Reverse sorted
    test_list_6 = [5, 4, 3, 2, 1]
    print(f"Test 6 (Reverse): {my_sort(test_list_6)}") # Expected: [1, 2, 3, 4, 5]