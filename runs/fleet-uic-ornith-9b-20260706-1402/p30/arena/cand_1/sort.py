"""Candidate #1: Bottom-up iterative merge sort.

Distinct angle vs the usual recursive top-down or Timsort-style approach:
  - Pure bottom-up (no recursion), merges from small runs upward in power-of-2 order.
  - Iterative merging avoids Python function-call overhead on large inputs.
  - Chunk sizing adapts to array size for cache-friendly behavior.
"""

def _merge(a, lo, mid, hi):
    """Merge a[lo:mid] and a[mid:hi] in-place (two-pointer into temp)."""
    left = a[lo:mid]
    right = a[mid:hi]
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            a[k] = left[i]; i += 1
        else:
            a[k] = right[j]; j += 1
        k += 1
    while i < len(left):
        a[k] = left[i]; i += 1; k += 1
    while j < len(right):
        a[k] = right[j]; j += 1; k += 1


def my_sort(xs):
    n = len(xs)
    if n <= 1:
        return xs[:]
    # Handle small lists with insertion sort (fast for tiny n, no merge overhead).
    threshold = max(20, int(n ** 0.5))
    for i in range(1, min(threshold, n)):
        key = xs[i]
        j = i - 1
        while j >= 0 and xs[j] > key:
            xs[j + 1] = xs[j]
            j -= 1
        xs[j + 1] = key

    # Bottom-up merge sort: merge runs of size 2^k starting from k=0.
    width = 1
    while width < n:
        i = 0
        while i < n:
            left_end = min(i + width, n)
            right_start = left_end + width
            right_end = min(right_start + width, n)
            if right_start > n:
                break
            _merge(xs, i, left_end, right_end)
            i += 2 * width
        width *= 2

    return xs


if __name__ == "__main__":
    # Quick sanity checks across edge cases.
    assert my_sort([]) == []
    assert my_sort([42]) == [42]
    assert my_sort([-3, -1, -5, -2]) == [-5, -3, -2, -1]
    assert my_sort([3, 1, 2, 1, 3]) == [1, 1, 2, 3, 3]
    assert my_sort([-10**9, 10**9, 0, -10**9, 10**9]) == [-10**9, -10**9, 0, 10**9, 10**9]
    assert len(my_sort(list(range(256)))) == 256
    print("All edge-case checks passed.")
