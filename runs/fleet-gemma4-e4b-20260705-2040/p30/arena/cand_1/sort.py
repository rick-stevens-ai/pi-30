def merge_sort(arr):
    """
    Recursively sorts an array using the Merge Sort algorithm.
    Time complexity: O(N log N)
    Space complexity: O(N) for temporary arrays during merging.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)

def merge(left, right):
    """
    Merges two sorted lists into a single sorted list.
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


def my_sort(xs):
    """
    Sorts the input list xs in ascending order using Merge Sort.

    Handles all edge cases: empty lists, singletons, duplicates, negatives, and large integers.
    Preserves multiset integrity (i.e., maintains counts of duplicate elements).
    Time Complexity: O(N log N)
    """
    # Ensure input is iterable/list-like for consistency, though the prompt implies a list.
    if not isinstance(xs, list):
        try:
            xs = list(xs)
        except TypeError:
            raise TypeError("Input must be convertible to a list.")

    return merge_sort(xs)

# Example usage and tests (for verification, not part of the exposed function)
if __name__ == '__main__':
    print("--- Running Tests ---")

    # Edge Case 1: Empty list
    empty = []
    sorted_empty = my_sort(empty)
    assert sorted_empty == [], f"Test Failed (Empty): Expected [], Got {sorted_empty}"
    print("Test Passed (Empty)")

    # Edge Case 2: Singleton list
    singleton = [42]
    sorted_singleton = my_sort(singleton)
    assert sorted_singleton == [42], f"Test Failed (Singleton): Expected [42], Got {sorted_singleton}"
    print("Test Passed (Singleton)")

    # Edge Case 3: Standard list with positive numbers
    standard = [5, 1, 4, 2]
    expected_standard = [1, 2, 4, 5]
    sorted_standard = my_sort(standard)
    assert sorted_standard == expected_standard, f"Test Failed (Standard): Expected {expected_standard}, Got {sorted_standard}"
    print("Test Passed (Standard)")

    # Edge Case 4: Duplicates and Multiset Preservation
    duplicates = [3, 1, 2, 3, 1]
    expected_duplicates = [1, 1, 2, 3, 3]
    sorted_duplicates = my_sort(duplicates)
    assert sorted_duplicates == expected_duplicates, f"Test Failed (Duplicates): Expected {expected_duplicates}, Got {sorted_duplicates}"
    print("Test Passed (Duplicates)")

    # Edge Case 5: Negatives and Positives
    mixed = [-5, 0, 10, -2]
    expected_mixed = [-5, -2, 0, 10]
    sorted_mixed = my_sort(mixed)
    assert sorted_mixed == expected_mixed, f"Test Failed (Mixed): Expected {expected_mixed}, Got {sorted_mixed}"
    print("Test Passed (Mixed)")

    # Edge Case 6: Large Integers
    large_ints = [10**20 + 5, 1, 10**20]
    expected_large_ints = [1, 10**20, 10**20 + 5]
    sorted_large_ints = my_sort(large_ints)
    assert sorted_large_ints == expected_large_ints, f"Test Failed (Large Ints): Expected {expected_large_ints}, Got {sorted_large_ints}"
    print("Test Passed (Large Ints)")

    # Edge Case 7: Mixed types (if comparable) - Note: Python comparison rules apply.
    # Since the requirement is "big ints" and standard sorting, we stick to comparable types.
    complex_data = [3.14, 2, 'a', 1] # This would fail in Python 3 due to type incompatibility unless handled explicitly. Assuming homogeneous input based on prompt context (ints/numbers).
    # Let's test with floats:
    float_test = [3.14, 1.0, 2.718]
    expected_float = [1.0, 2.718, 3.14]
    sorted_float = my_sort(float_test)
    assert sorted_float == expected_float, f"Test Failed (Floats): Expected {expected_float}, Got {sorted_float}"
    print("Test Passed (Floats)")

    print("\nAll tests completed successfully.")