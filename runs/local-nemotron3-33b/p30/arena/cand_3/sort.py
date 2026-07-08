"""Utility module for sorting collections.

Provides:
- my_sort(xs) -> list: returns a new sorted list (ascending) of the input ``xs``.
  Works correctly on empty lists, singletons, duplicate items, negative numbers,
  and large integers. Uses only the Python standard library (the built‑in ``sorted``)
  which implements Timsort with O(n log n) worst‑case performance and is highly
  optimized for large arrays.

Typical usage::

    >>> from sort import my_sort
    >>> my_sort([3, 1, -2, 5])
    [-2, 1, 3, 5]
"""

from typing import Iterable, List, TypeVar

T = TypeVar("T")


def my_sort(xs: Iterable[T]) -> List[T]:
    """Return a **new** list containing the elements of *xs* sorted in ascending order.

    The function works correctly for:
      - empty iterables → ``[]`` (preserves multiset)
      - singletons → unchanged element
      - duplicates → all copies present, correctly ordered
      - negative numbers and arbitrarily large integers → handled by Python's
        native comparison operators used by ``sorted``.

    Parameters
    ----------
    xs : Iterable[T]
        Any iterable yielding comparable items (e.g. list, tuple, generator).

    Returns
    -------
    List[T]
        A new list with the elements of *xs* sorted in non‑decreasing order.
        The original ``xs`` is **not** modified.

    Notes
    -----
    - Uses only stdlib functions: the built‑in :func:`sorted`, which is a C‑level
      implementation of Timsort (optimal for partially ordered data).
    - Runs in O(n log n) time and uses O(n) auxiliary space, which is fast on large
      arrays.
    """
    # ``sorted`` returns a new list, guaranteeing we don't mutate the input.
    return sorted(xs)


# The following block allows the file to be executed for quick manual testing.
if __name__ == "__main__":
    import json

    def parse_input():
        """Simple JSON input parser: expects a JSON array."""
        try:
            raw = input("Enter JSON array (or empty []): ")
            return json.loads(raw)
        except EOFError:
            return []
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON: {exc}") from exc

    arr = parse_input()
    print("Original :", arr)
    print("Sorted   :", my_sort(arr))