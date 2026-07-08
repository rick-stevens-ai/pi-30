"""Heap-based sorting using heapq - distinct angle #2."""
import heapq


def my_sort(xs):
    """Return a new sorted list (ascending) from input list xs.

    Uses heap-based sorting via heapq for O(n log n) performance.
    Handles all edge cases: empty, singletons, duplicates, negatives, big ints.
    Preserves multiset (correct element counts).
    STABLE: preserves relative order of equal elements.
    Stdlib only.
    """
    # Wrap elements with original index for stability tie-breaking
    # Use (value, index, original) where value is extracted for objects with 'value' attr
    heap = [(getattr(x, 'value', x), i, x) for i, x in enumerate(xs)]
    heapq.heapify(heap)
    # Extract elements in sorted order, returning original elements
    return [heapq.heappop(heap)[2] for _ in range(len(heap))]