def my_sort(xs):
    """Return a new list containing the elements of *xs* sorted in ascending order.

    Works for:
        - empty iterable → []
        - singletons   → unchanged element
        - duplicates   → multiset preserved (order of equal items stable)
        - negative numbers and arbitrarily large integers or other comparable objects.
    """
    return sorted(xs)