"""Candidate #3: Stdlib-only, maximal speed via built-in Timsort (C-optimized)."""

def my_sort(xs):
    """Return a new list containing the elements of xs in ascending order.

    Correct on all edge cases (empty, singletons, duplicates, negatives, big ints),
    preserves multiset (equal elements retain original order - stable sort),
    and is maximally fast on large arrays by delegating to CPython's C-optimized
    Timsort via the built-in sorted().
    """
    return sorted(xs)


if __name__ == "__main__":
    # Quick self-test
    assert my_sort([]) == []
    assert my_sort([1]) == [1]
    assert my_sort([3, 1, 2]) == [1, 2, 3]
    assert my_sort([3, 1, 2, 1]) == [1, 1, 2, 3]  # dupes preserved
    assert my_sort([-5, 3, -2, 0]) == [-5, -2, 0, 3]  # negatives
    assert my_sort([10**100, 1, 10**50]) == [1, 10**50, 10**100]  # big ints
    # Stability: equal elements preserve original order
    assert my_sort([(2, 'a'), (1, 'b'), (2, 'c')]) == [(1, 'b'), (2, 'a'), (2, 'c')]
    print("All tests passed!")