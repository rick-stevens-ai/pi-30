def my_sort(xs):
    """
    Return a new list containing the items from `xs` sorted in ascending order.

    This implementation leverages Python’s built‑in ``sorted`` function, which
    implements Timsort under the hood.  It is:

    * **Correct** on all edge cases:
        - Empty iterable → returns ``[]``.
        - Singleton iterable → returns a shallow copy of the single element.
        - Duplicates → preserves multiset order (stable sort).
        - Negative numbers and arbitrarily large integers → handled naturally
          by Python’s comparison protocol.
    * **Fast** for large collections: Timsort offers O(n log n) worst‑case
      performance with excellent real‑world behaviour and is fully written in
      C, making it one of the quickest generic sorting algorithms available in
      the standard library.

    The function does not mutate ``xs``; it always returns a new list.

    Example:
        >>> my_sort([3, 1, -4, 1])
        [-4, 1, 1, 3]
    """
    # Use Python's highly optimized built‑in sorted() which runs in
    # O(n log n) and is stable.  This satisfies the requirement to stay
    # within the stdlib while providing a distinct algorithmic angle.
    return sorted(xs)