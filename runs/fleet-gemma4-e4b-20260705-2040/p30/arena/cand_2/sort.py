def my_sort(xs):
    """
    Sorts a list xs in ascending order using Merge Sort.

    This implementation is stable and handles all specified edge cases 
    (empty, singletons, duplicates, negatives, big integers) while maintaining 
    multiset integrity. Time complexity: O(N log N). Uses only standard library features.
    """
    n = len(xs)
    if n <= 1:
        return xs

    mid = n // 2
    left_half = my_sort(xs[:mid])
    right_half = my_sort(xs[mid:])

    # Merge the two sorted halves
    merged = []
    i = j = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:  # Stability check: use <= for stability
            merged.append(left_half[i])
            i += 1
        else:
            merged.append(right_half[j])
            j += 1

    # Append remaining elements
    merged.extend(left_half[i:])
    merged.extend(right_half[j:])

    return merged

if __name__ == '__main__':
    # Test Cases
    tests = {
        "Empty list": [],
        "Single element": [42],
        "Sorted list": [1, 2, 3, 4, 5],
        "Reverse sorted list": [5, 4, 3, 2, 1],
        "Duplicates": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
        "Negatives only": [-5, -10, -1, -8],
        "Mixed (pos/neg)": [-5, 1, 0, -100, 50],
        "Big integers": [999999999999, 1, 2, 3],
        "All same": [7, 7, 7]
    }

    print("--- Running my_sort tests ---")
    all_passed = True
    for name, input_list in tests.items():
        try:
            sorted_list = my_sort(input_list)
            expected_output = sorted(input_list) # Using standard library sort for verification
            
            assert sorted_list == expected_output, f"Test '{name}' FAILED: Input {input_list}, Got {sorted_list}, Expected {expected_output}"
            print(f"✅ Test '{name}' PASSED.")
        except AssertionError as e:
            print(f"❌ Test '{name}' FAILED. Details: {e}")
            all_passed = False
        except Exception as e:
            print(f"❌ Test '{name}' CRASHED with error: {e}")
            all_passed = False

    if all_passed:
        print("\nAll tests passed successfully.")
    else:
        print("\nSome tests failed.")