def my_sort(xs):
    """
    Returns a new sorted list (ascending) from the input iterable xs.

    This implementation leverages Python's built-in `sorted()` function, 
    which utilizes the Timsort algorithm. Timsort is highly optimized in C 
    and provides O(n log n) worst-case and O(n) best-case time complexity.

    Correctness:
    - Empty input: Returns an empty list.
    - Singletons: Returns a new list with the single element.
    - Duplicates: Preserves all duplicates (multiset property).
    - Negatives & Big Ints: Handled correctly by Python's integer type.
    - Stability: Timsort is stable, preserving the relative order of equal elements.

    Complexity:
    - Time: O(n log n) worst case, O(n) best case.
    - Space: O(n) to create the new list.

    Args:
        xs (iterable): The input collection to sort.

    Returns:
        list: A new sorted list containing all elements from xs.
    """
    return sorted(xs)

if __name__ == "__main__":
    # Quick test cases
    assert my_sort([]) == []
    assert my_sort([1]) == [1]
    assert my_sort([3, 1, 2]) == [1, 2, 3]
    assert my_sort([2, 2, 1, 1]) == [1, 1, 2, 2]
    assert my_sort([-1, -5, 0, 5, 1]) == [-5, -1, 0, 1, 5]
    assert my_sort([10**20, 1, 10**10]) == [1, 10**10, 10**20]
    print("All basic tests passed!")
