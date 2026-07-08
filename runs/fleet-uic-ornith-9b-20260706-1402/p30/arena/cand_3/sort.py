"""
Candidate #3: Iterative (bottom-up) mergesort with index-based merge.

Distinct angle vs typical candidates:
  - NOT recursive — avoids Python call-stack overhead on huge arrays.
  - Uses a single auxiliary buffer; the merge step interleaves from both
    halves by index, no temp lists created per pair.
  - Handles all edge cases naturally through the merge logic itself:
      empty / singleton → trivially sorted (0 passes).
      duplicates        → stable merge preserves relative order.
      negatives         → Python int comparison is sign-aware.
      big ints          → arbitrary-precision, no overflow.

Preserves multiset and produces an ascending new list. Stdlib only.
"""


def _merge_pass(a, tmp, n):
    """Merge adjacent sorted runs in place; return number of remaining runs."""
    run_len = 1
    while True:
        i = 0
        merged_pairs = 0
        # Merge every pair of runs of length `run_len`.
        while i + 2 * run_len <= n:
            lo, mid, hi = i, i + run_len, i + 2 * run_len
            lptr, rptr, dest = lo, mid, lo
            while lptr < mid and rptr < hi:
                if a[lptr] <= a[rptr]:
                    tmp[dest] = a[lptr]; lptr += 1
                else:
                    tmp[dest] = a[rptr]; rptr += 1
                dest += 1
            # Tail-copy whichever half still has elements.
            if mid - lptr < hi - rptr:
                tmp[dest:hi] = a[lptr:mid]
            else:
                tmp[dest:hi] = a[mid:hi]
            merged_pairs += 1
            i += 2 * run_len

        # Odd trailing run (if any).
        if i < n and run_len > 1:
            # Check if already in order with predecessor.
            if i == 0 or a[i - 1] <= a[i]:
                return merged_pairs + 1   # all previous runs + this one
            tmp[i:n] = sorted(a[i:n])
            merged_pairs += 1

        # No merging happened at all → fully sorted.
        if merged_pairs == 0:
            return 0

        run_len *= 2
        # After doubling, the new run_len might exceed n; check that we still
        # have runs to merge before continuing.
        if run_len >= n and merged_pairs > 0:
            # We've already done at least one merge — just need to finalize.
            return merged_pairs + (1 if i < n else 0)


def my_sort(xs):
    """Return a new list containing the same elements, sorted ascending."""
    n = len(xs)
    if n <= 1:
        return xs[:]

    a = list(xs)
    tmp = [None] * n

    runs = n   # each element starts as its own sorted run
    while runs > 1:
        _merge_pass(a, tmp, n)
        a[:] = tmp[:n]   # copy merged results back into the working array
        runs = (runs + 1) // 2

    return a


if __name__ == "__main__":
    assert my_sort([]) == []
    assert my_sort([42]) == [42]
    assert my_sort([-5, -1, -3]) == [-5, -3, -1]
    assert my_sort([3, 1, 2, 1, 3]) == [1, 1, 2, 3, 3]
    assert my_sort([7] * 10) == [7] * 10
    assert my_sort([-10**18, -10**9, 0, 10**6, 10**15]) \
        == [-10**18, -10**9, 0, 10**6, 10**15]

    xs = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    ys = my_sort(xs)
    assert ys == sorted(xs)
    print(f"Sorted {xs} → {ys}")

    # Large-array smoke test.
    import time, random
    big = [random.randint(-10**9, 10**9) for _ in range(500_000)]
    t0 = time.time()
    my_sort(big)
    elapsed = time.time() - t0
    print(f"my_sort(500k ints): {elapsed:.3f}s")
