"""
Candidate #2: HeapSort via heapq — stdlib's C-optimised priority queue.

Distinct angle from typical quicksort/mergesort candidates: instead of writing
a comparison-based loop, we treat the array as a min-heap and repeatedly extract
the smallest element. Complexity is O(n log n), but the hot path (heappop) runs
in C — far faster than any pure-Python sort implementation.

Correct on every edge case; preserves multiset exactly.
"""


import heapq


def my_sort(xs):
    if not xs:
        return []
    arr = list(xs)                      # defensive copy — caller's data untouched
    heapq.heapify(arr)                  # O(n)  → min-heap in-place (C-level)
    return [heapq.heappop(arr) for _ in range(len(arr))]   # O(n log n)


if __name__ == "__main__":
    import random, time

    rng = random.Random(42)

    # correctness smoke test
    for seed in range(50):
        xs = [rng.randint(-1_000_000, 1_000_000) for _ in range(rng.randint(0, 30))]
        assert my_sort(xs) == sorted(xs), f"FAIL seed {seed}"

    # edge cases
    assert my_sort([]) == []
    assert my_sort([42]) == [42]
    assert my_sort([-5, -1, -3, -7]) == [-7, -5, -3, -1]
    assert my_sort([3, 1, 2, 1, 1, 2, 3]) == [1, 1, 1, 2, 2, 3, 3]
    assert my_sort([9**100, -(9**100), 0]) == [-(9**100), 0, 9**100]

    # speed test — large array
    big = [rng.randint(-10_000, 10_000) for _ in range(2_000_000)]
    t0 = time.perf_counter()
    my_sort(big)
    elapsed = time.perf_counter() - t0
    print(f"HeapSort 2M ints: {elapsed:.3f}s")
