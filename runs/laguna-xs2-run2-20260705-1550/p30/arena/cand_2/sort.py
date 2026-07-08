"""Merge sort implementation - stable, O(n log n), handles all edge cases."""


def my_sort(xs):
    """Return a new sorted list (ascending).
    
    Handles: empty lists, singletons, duplicates, negatives, big ints.
    Preserves multiset. Uses only stdlib.
    """
    def merge(left, right):
        """Merge two sorted lists into one sorted list."""
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def sort(arr):
        """Recursively sort array using merge sort."""
        if len(arr) <= 1:
            return list(arr)
        mid = len(arr) // 2
        return merge(sort(arr[:mid]), sort(arr[mid:]))
    
    return sort(xs)