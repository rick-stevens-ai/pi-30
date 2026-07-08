def my_sort(xs):
    """
    Sorts a list using the Heap Sort algorithm.
    Heap sort provides O(n log n) worst-case time complexity and 
    is distinct from common Merge or Quick sort implementations.
    It preserves multisets and handles all edge cases correctly.
    """
    # Handle empty or single-element lists
    if len(xs) <= 1:
        return list(xs)

    # Work on a copy to preserve the original list (as per requirements)
    arr = list(xs)
    n = len(arr)

    def heapify(n, i):
        while True:
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2

            if l < n and arr[l] > arr[largest]:
                largest = l

            if r < n and arr[r] > arr[largest]:
                largest = r

            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                i = largest
            else:
                break

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # One by one extract elements from the heap
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(i, 0)

    return arr

if __name__ == "__main__":
    # Test cases
    test_cases = [
        ([], []),
        ([5], [5]),
        ([3, 1, 2], [1, 2, 3]),
        ([3, 2, 1, 2], [1, 2, 2, 3]),
        ([-5, 0, 5, -2], [-5, -2, 0, 5]),
        ([10**18, 10**18 + 1, 10**18 - 1], [10**18 - 1, 10**18, 10**18 + 1]),
    ]

    for input_xs, expected in test_cases:
        result = my_sort(input_xs)
        assert result == expected, f"Failed on {input_xs}: expected {expected}, got {result}"

    # Large array test
    large_arr = list(range(10000, 0, -1))
    sorted_large_arr = my_sort(large_arr)
    assert sorted_large_arr == list(range(1, 10001)), "Large array test failed"

    print("All tests passed!")
