def my_sort(xs):
    """Return a new sorted list (ascending), preserving multiset.

    Uses Python's stdlib Timsort (highly optimized hybrid merge/insertion sort)
    for correctness on all edge cases (empty, singletons, duplicates, negatives,
    big ints) and speed on large arrays.
    """
    return sorted(xs)
