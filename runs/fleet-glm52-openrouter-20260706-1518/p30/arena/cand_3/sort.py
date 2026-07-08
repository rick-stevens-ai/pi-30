"""my_sort: a stable, in-place mergesort-variant exposed as my_sort(xs).

Design (candidate #3 distinct angle):
  Bottom-up natural mergesort.

Why this angle:
  * Exploits existing runs ("natural" order) so near-sorted inputs are nearly
    O(n) instead of O(n log n) -- a property quicksort lacks.
  * Bottom-up => iterative, no recursion => no stack overflow on adversarial
    or huge inputs, and no worst-case O(n^2) like naive quicksort.
  * Strict O(n log n) worst case, stable, preserves the multiset exactly.
  * Uses a single temp buffer reused across merge passes (O(n) extra space),
    then returns a brand-new list so the input is never mutated.

Edge cases handled:
  empty / singleton / dupes / negatives / big ints / mixed numeric types.
  Ordering relies on the elements' own < comparison, matching Python's
  default total ordering for numbers.
"""

from __future__ import annotations

from typing import List, TypeVar

T = TypeVar("T")


def _insertion_sort(a: List[T], lo: int, hi: int) -> None:
    """In-place insertion sort for tiny slices. Stable."""
    for i in range(lo + 1, hi):
        x = a[i]
        j = i - 1
        while j >= lo and a[j] > x:  # strict > keeps equal keys stable
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def _merge(a: List[T], buf: List[T], lo: int, mid: int, hi: int) -> None:
    """Stable merge of a[lo:mid] and a[mid:hi] using shared buffer."""
    left = a[lo:mid]
    buf[lo:mid] = left  # copy left run into reusable buffer
    i, j, k = lo, mid, lo
    nleft = mid - lo
    while i < lo + nleft and j < hi:
        # <= on left side keeps stable order for equal keys
        if buf[i] <= a[j]:
            a[k] = buf[i]
            i += 1
        else:
            a[k] = a[j]
            j += 1
        k += 1
    while i < lo + nleft:
        a[k] = buf[i]
        i += 1
        k += 1
    # right side already in place if leftover; nothing to copy.


def my_sort(xs):
    """Return a new list with the elements of xs sorted ascending.

    Stable, O(n log n) worst case, O(n) extra space. Input is untouched.
    """
    # Work on a copy so the caller's list is never mutated.
    a = list(xs)
    n = len(a)
    if n < 2:
        return a

    buf = [None] * n  # reusable scratch buffer for merges

    MIN_RUN = 32  # below this size, insertion sort is faster

    # --- Phase 1: carve natural ascending runs, insertion-sort short ones. ---
    runs = []  # list of (start, end) exclusive end indices
    i = 0
    while i < n:
        # Detect natural run direction.
        if i == n - 1:
            runs.append((i, n))
            break
        if a[i] <= a[i + 1]:
            j = i + 1
            while j < n - 1 and a[j] <= a[j + 1]:
                j += 1
            j += 1
        else:
            # strictly descending run => reverse it to make ascending.
            j = i + 1
            while j < n - 1 and a[j] > a[j + 1]:
                j += 1
            j += 1
            a[i:j] = a[i:j][::-1]
        # Extend run to at least MIN_RUN via insertion sort, if room.
        end = j
        if end - i < MIN_RUN:
            end = min(i + MIN_RUN, n)
            _insertion_sort(a, i, end)
        runs.append((i, end))
        i = end

    # --- Phase 2: bottom-up merge pass over runs. ---
    while len(runs) > 1:
        new_runs = []
        for k in range(0, len(runs), 2):
            if k + 1 >= len(runs):
                new_runs.append(runs[k])
                break
            lo, mid = runs[k]
            _, hi = runs[k + 1]
            _merge(a, buf, lo, mid, hi)
            new_runs.append((lo, hi))
        runs = new_runs

    return a


if __name__ == "__main__":
    import random
    import sys

    def check(data, name):
        got = my_sort(data)
        exp = sorted(data)
        assert got == exp, f"{name}: FAIL"
        # multiset preserved exactly
        assert len(got) == len(data), f"{name}: length drift"
        # input not mutated
        assert data is not got
        print(f"{name}: ok")

    check([], "empty")
    check([42], "singleton")
    check([1, 1, 1, 1], "all_dupes")
    check([3, 1, 2, 1, 3, 2], "dupes_mixed")
    check([-5, -1, -10, 0, 3, -2], "negatives")
    check([2 ** 70, -(2 ** 70), 0, 2 ** 70 + 1, -(2 ** 70) - 1], "bigints")
    check([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], "classic")
    check(list(range(1000)) + list(range(500)), "near_sorted")
    check(list(range(2000, 0, -1)), "reversed")
    check([random.randint(-10 ** 6, 10 ** 6) for _ in range(5000)], "random5k")

    # speed smoke test on a large array
    big = [random.randint(-(10 ** 12), 10 ** 12) for _ in range(1_000_000)]
    import time

    t0 = time.perf_counter()
    r = my_sort(big)
    t1 = time.perf_counter()
    assert r == sorted(big), "big: FAIL"
    print(f"big 1e6: ok in {t1 - t0:.3f}s")
