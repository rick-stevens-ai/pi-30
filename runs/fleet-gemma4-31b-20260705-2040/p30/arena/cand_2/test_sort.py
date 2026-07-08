def my_sort(xs):
    """
    Sorts a list in ascending order using a stable Merge Sort algorithm.
    Returns a new sorted list.
    
    Args:
        xs (list): The list of elements to be sorted.
        
    Returns:
        list: A new sorted list containing all elements from the original multiset.
    """
    # Handle edge cases: empty or single-element lists
    if len(xs) <= 1:
        return list(xs)

    def merge(left, right):
        result = []
        i = j = 0
        len_l, len_r = len(left), len(right)
        
        while i < len_l and j < len_r:
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Append remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort_recursive(arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        # Slicing creates new lists, ensuring we don't mutate the original input
        left = sort_recursive(arr[:mid])
        right = sort_recursive(arr[mid:])
        
        return merge(left, right)

    return sort_recursive(list(xs))

def test():
    test_cases = [
        ([], []), # Empty
        ([1], [1]), # Single element
        ([2, 1], [1, 2]), # Simple unsorted
        ([1, 2], [1, 2]), # Already sorted
        ([2, 1, 3, 0], [0, 1, 2, 3]), # Mixed
        ([-1, -5, 0, 5, 1], [-5, -1, 0, 1, 5]), # Negatives
        ([1, 2, 1, 2, 1], [1, 1, 1, 2, 2]), # Duplicates
    ]
    
    for input_val, expected in test_cases:
        actual = my_sort(input_val)
        assert actual == expected, f"Failed for {input_val}: expected {expected}, got {actual}"

    # Stability check: sort list of tuples by first element
    stability_input = [(1, 'a'), (2, 'b'), (1, 'c'), (0, 'd')]
    # Expected order if stable: (0, 'd'), (1, 'a'), (1, 'c'), (2, 'b')
    # But wait, my_sort uses standard comparison. For tuples, it compares element by element.
    # To test stability properly, we need a custom key or just rely on the fact that 
    # Merge Sort is stable if it preserves relative order of equal elements.
    
    # Let's redefine a version of my_sort that takes a key to test stability
    def my_sort_key(xs, key=lambda x: x):
        if len(xs) <= 1:
            return list(xs)

        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if key(left[i]) <= key(right[j]):
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        def sort_recursive(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = sort_recursive(arr[:mid])
            right = sort_recursive(arr[mid:])
            return merge(left, right)

        return sort_recursive(list(xs))

    stability_input = [(1, 'a'), (2, 'b'), (1, 'c'), (0, 'd')]
    expected_stable = [(0, 'd'), (1, 'a'), (1, 'c'), (2, 'b')]
    actual_stable = my_sort_key(stability_input, key=lambda x: x[0])
    assert actual_stable == expected_stable, f"Stability failed: expected {expected_stable}, got {actual_stable}"

    print("All tests passed!")

if __name__ == "__main__":
    test()
