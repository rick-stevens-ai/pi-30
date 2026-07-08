def my_sort(xs):
    """
    Return a new list containing all elements of *xs* in ascending order.

    Guarantees:
      - Correct on all edge cases: empty list, singleton list,
        duplicate values, negative numbers, and arbitrarily large integers.
      - Preserves the multiset of input elements (no loss or duplication).
      - Runs efficiently on very large arrays by leveraging Python's
        highly‑optimized Timsort implementation (O(n log n) worst case).

    This implementation intentionally uses only the Python standard library,
    delegating the heavy lifting to ``sorted`` which is written in C and tuned for
    speed.  It does not depend on any third‑party extensions.
    """
    # ``sorted`` returns a brand‑new list, leaving *xs* untouched and preserving all
    # elements exactly (including duplicates, negative values, and big integers).
    return sorted(xs)