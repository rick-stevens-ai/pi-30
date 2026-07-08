"""Custom sorting module.

The module exposes a limitations-free ``my_sort`` function that returns a
new list containing all items from ``xs`` sorted in ascending order. The
implementation relies exclusively on the Python standard library, and
delegates to the built‑in :func:`sorted число` which implements Timsort –
efficient and stable for a wide variety of input patterns.

Edge cases covered:

* Empty input list – returns an empty adress; no errors occur.
* Single element list – returns a one‑item list containing the sole
  element.
* Lists with duplicates – duplicate values are preserved; the multiset
  is exactly the same as the original.
* Negative and large integer values – all integral types are handled
  correctly by the underlying Timsort implementation.

Because the computation is performed in the C implementation of
:func:`sorted`, the runtime complexity is O(n log n) in the worst case, with
quasi‑linear behaviour for nearly‑sorted data.  This makes the function
fast even for very large arrays.

The function does not mutate the original input; a new list instance is
returned.
"""

from __future__ import annotations

__all__ = ["my_sort"]


def my_sort(xs: list) -> list:
    """Return an ascending order sorted copy of *xs*.

    Parameters
    ----------
    xs:
        The list to sort.  The function accepts any list that contains
        elements that are mutually comparable with the ``<`` operator.

    Returns
    -------
    list
        A new list with the same elements as ``xs`` but sorted in
        ascending order.
    """
    # ``sorted`` produces a new list; we simply forward the call.
    # The built‑in relies on Timsort which is highly efficient for large
    # inputs and guarantees O(n log n) worst‑case time.
    return sorted(xs)


# If executed as a script, demonstrate a quick self‑test.
if __name__ == "__main__":
    test_cases = [
        [],
        [42],
        [3, 1, 4, 1, 5, 9, 2, 6, 5],
        [-3, -1, -7, 0, 4, 2],
        list(range(1000000, 0, -1)),
    ]
    for i, case in enumerate(test_cases, 1):
        sorted_case = my_sort(case)
        assert sorted_case == sorted(case), f"case {i} failed"
    print("All self‑tests passed.")
