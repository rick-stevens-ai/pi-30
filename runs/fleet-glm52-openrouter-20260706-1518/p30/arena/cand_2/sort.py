"""my_sort: correct, fast, ascending sort returning a new list.

Design (Candidate #2, distinct angle):
    Comparison-based sorting via the stdlib's Timsort (``sorted``).

    Why comparison-based rather than counting/radix?
        Counting sort blows up (memory/time) on sparse or wide ranges and on
        big ints; radix sort needs a per-pass digit model that breaks for
        arbitrary-precision integers and is tricky to get right for negatives.
        A comparison-based sort is *unconditionally* correct for empty lists,
        singletons, duplicates, negatives, and big ints -- the exact edge
        cases we must pass -- while still running in O(n log n) and, because
        Timsort is implemented in C, staying fast on large arrays.

Contract:
    * Input: any iterable of orderable elements.
    * Output: a NEW list sorted ascending; the input is never mutated.
    * Stability: Timsort is stable, so equal keys keep their relative order.
"""

from __future__ import annotations

from typing import Iterable, List, TypeVar

_T = TypeVar("_T")


def my_sort(xs: Iterable[_T]) -> List[_T]:
    """Return a new list with the elements of ``xs`` in ascending order.

    Handles every edge category correctly:
        * empty iterable          -> []
        * singletons              -> single-element list
        * duplicates              -> multiset preserved (stable)
        * negatives               -> ordered by value
        * arbitrary big ints      -> exact (no float/overflow)
    The input iterable is never mutated; a fresh list is always returned.
    """
    # ``sorted`` materializes a new list from any iterable and sorts it in
    # place before returning it. It raises TypeError naturally if elements
    # are not mutually orderable, which is the correct, safe failure mode.
    return sorted(xs)


if __name__ == "__main__":  # pragma: no cover - lightweight self-check
    # Quick edge-case sanity checks.
    assert my_sort([]) == []
    assert my_sort([1]) == [1]
    assert my_sort([3, 1, 2]) == [1, 2, 3]
    assert my_sort([2, 2, 1, 1]) == [1, 1, 2, 2]            # dupes / multiset
    assert my_sort([-3, 0, -1, 2]) == [-3, -1, 0, 2]        # negatives
    assert my_sort([10**100, 1, 10**100 + 1]) == [1, 10**100, 10**100 + 1]
    # Non-mutation guarantee.
    src = [3, 1, 2]
    _ = my_sort(src)
    assert src == [3, 1, 2]
    # Iterable (not just list) input.
    assert my_sort((x for x in "bca")) == ["a", "b", "c"]
    print("all self-checks passed")
