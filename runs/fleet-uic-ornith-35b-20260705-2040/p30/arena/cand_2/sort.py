"""
sort.py — Candidate #2: heapsort via heapq (O(n log n) worst-case guaranteed).

Distinct angle: instead of divide-and-conquer (timsort/mergesort), we use the
implicit-min-heap data structure. This gives a *guaranteed* O(n log n) worst case,
unlike adaptive sorts that degrade on pathological inputs — and `heapq` is C-implemented
in CPython so real-world throughput stays high on large arrays.

Edge cases handled naturally: empty → heapify yields [] → returns []; singletons iterate once;
duplicates stay (multiset preserved); negatives sort correctly via total order.
"""

from heapq import heapify, heappop


def my_sort(xs):
    """Return a new list with the elements of xs sorted in ascending order."""
    # Build a min-heap over a *copy* so the input is never mutated.
    heap = list(xs)  # O(n): shallow copy (cheap for int/float scalars)
    heapify(heap)    # O(n): Floyd's algorithm — cheaper than n× heappush

    out = []
    heappop_append = out.append   # local-name binding: avoids per-call attribute lookup in tight loop
    while heap:                   # ~n iterations × O(log n) heappop work
        heappop_append(heappop(heap))
    return out


# --- lightweight sanity checks (stdlib only, fast path for small inputs / tests) --------------------------
if __name__ == "__main__":
    cases = [
        [],                        # empty
        [1],                       # singleton
        [2, 1],                    # two-element reverse
        [5, 3, 1, 4, 2],           # basic random-ish
        list(range(9, -1, -1)),    # full reversal of 0..9
        [3, 3, 3, 1, 1, 5, 2, 2],  # heavy duplicates + negatives? (no negatives here)
        [-5, 0, -5, 7, -100, 42],  # negatives
        [10**18, -(10**18), 0],    # big ints
    ]

    for c in cases:
        assert my_sort(c) == sorted(c), f"FAIL on {c}"

    import time, random
    rng = random.Random(0)
    big = [rng.randrange(-(10**12), 10**12) for _ in range(5_000_000)]
    t0 = time.time()
    r = my_sort(big)
    elapsed = time.time() - t0
    assert r == sorted(big), "mismatch vs built-in"
    assert len(r) == 5_000_000
    from collections import Counter
    assert Counter(r) == Counter(big), "multiset mismatch!"
    print(f"5,000,000 random ints sorted in {elapsed:.2f}s")
