"""Heap-based sorting using heapq (Candidate #3 distinct angle).

This implementation uses a min-heap to sort elements. It:
- Returns a new sorted list (ascending)
- Handles all edge cases: empty, singletons, duplicates, negatives, big ints
- Preserves multiset (same elements, same counts)
- Runs in O(n log n) time
- Uses only stdlib (heapq)
"""

import heapq


def my_sort(xs):
    """Return a new list with elements from xs sorted in ascending order.

    Args:
        xs: An iterable of comparable elements (numbers, etc.)

    Returns:
        A new list containing all elements from xs in ascending order.

    Examples:
        >>> my_sort([3, 1, 4, 1, 5])
        [1, 1, 3, 4, 5]
        >>> my_sort([])
        []
        >>> my_sort([-5, 0, 5])
        [-5, 0, 5]
        >>> my_sort([2**100, 1])
        [1, 1267650600228229401496703205376]
    """
    # Handle edge case: empty input
    if not xs:
        return []

    # Create a min-heap from the input (copies the list)
    heap = list(xs)
    heapq.heapify(heap)

    # Extract elements in sorted order
    result = []
    while heap:
        result.append(heapq.heappop(heap))

    return result