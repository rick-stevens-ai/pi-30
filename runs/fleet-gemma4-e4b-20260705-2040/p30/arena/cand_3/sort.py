def my_sort(xs):
    """
    Sorts a list of elements in ascending order using Merge Sort, 
    ensuring correctness across edge cases and high performance (O(N log N)).

    Args:
        xs: The input list.

    Returns:
        A new sorted list.
    """
    if len(xs) <= 1:
        return xs[:]  # Return a copy for consistency

    mid = len(xs) // 2
    left = my_sort(xs[:mid])
    right = my_sort(xs[mid:])

    # Merge step
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
    import random
    import time

    def test_sort(test_name, data):
        print(f"--- Running Test: {test_name} ---")
        original = list(data)
        start_time = time.perf_counter()
        sorted_list = my_sort(original)
        end_time = time.perf_counter()

        # Verification checks
        is_sorted = all(sorted_list[i] <= sorted_list[i+1] for i in range(len(sorted_list) - 1))
        preserves_multiset = sorted(original) == sorted_list
        
        print(f"Time taken: {end_time - start_time:.6f} seconds")
        print(f"Is correctly sorted? {is_sorted}")
        print(f"Preserves multiset? {preserves_multiset}")

    # Edge Case Tests
    test_sort("Empty List", [])
    test_sort("Singleton List (Positive)", [5])
    test_sort("Singleton List (Negative)", [-10])
    test_sort("All Duplicates", [3, 3, 3, 3])
    test_sort("All Negatives", [-5, -2, -8, -2])
    test_sort("Mixed Positives/Negatives", [5, -1, 0, 10, -5])
    test_sort("Big Integers", [999999999999999, 1, 0, -1, -999999999999999])

    # Large Array Test (Performance Check)
    print("\n--- Running Performance Test (N=10^5) ---")
    large_data = [random.randint(-10**9, 10**9) for _ in range(100000)]
    test_sort("Large Random Array", large_data)

    # Complex Duplicates/Order Test
    complex_dupes = [5, 2, 8, 2, 5, 1, 8]
    test_sort("Complex Duplicates and Order", complex_dupes)