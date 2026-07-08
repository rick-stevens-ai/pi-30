def my_sort(xs):
    """Return a new list containing the items from *xs* sorted in ascending order.

    This implementation uses Python's built-in Timsort, which is stable.
    The original list remains untouched.

    Edge cases handled:
      - empty input → []
      - singleton input → [item]
      - duplicates → relative order of equal elements is preserved
      - negative numbers and arbitrarily large integers → handled correctly

    It relies on the Python standard library's sorted() function, which guarantees O(n log n)
    performance and stability.
    """
    return sorted(xs)