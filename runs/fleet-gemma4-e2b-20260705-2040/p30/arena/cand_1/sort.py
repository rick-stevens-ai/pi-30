def my_sort(xs: list) -> list:
    """
    Sorts a list of comparable elements in ascending order using the Merge Sort algorithm.

    This implementation is O(n log n) time complexity and preserves the multiset,
    handling all edge cases (empty list, singletons, negatives, large ints).
    It returns a new sorted list.

    Args:
        xs: The list of elements to be sorted.

    Returns:
        A new list containing the elements of xs sorted in ascending order.
    """
    n = len(xs)
    if n <= 1:
        return xs

    mid = n // 2
    left_half = xs[:mid]
    right_half = xs[mid:]

    # Recursively sort the halves
    left = my_sort(left_half)
    right = my_sort(right_half)

    # Merge the sorted halves
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
    print("Test 1 (Empty):", my_sort([]))
    print("Test 2 (Singletons):", my_sort([5]))
    print("Test 3 (Duplicates):", my_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]))
    print("Test 4 (Negatives/Mixed):", my_sort([-5, 10, -1, 0, 3, -2]))
    print("Test 5 (Large Ints):", my_sort([10**9, 0, -10**9, 500]))
    print("Test 6 (Already Sorted):", my_sort([1, 2, 3, 4, 5]))
    print("Test 7 (Reverse Sorted):", my_sort([5, 4, 3, 2, 1]))