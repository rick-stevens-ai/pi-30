def my_sort(xs):
    """Sort a list in ascending order. Returns a new sorted list (ascending).

    Handles empty lists, singletons, duplicates, negatives, big ints — all
    correctly via an O(n log n) merge sort that preserves the multiset.
    Uses only stdlib.
    """
    if not xs:
        return []

    def _merge(left, right):
        i = j = 0
        out = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        out.extend(left[i:])
        out.extend(right[j:])
        return out

    def _merge_sort(arr):
        n = len(arr)
        if n <= 1:
            return arr[:]
        mid = n // 2
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])
        return _merge(left, right)

    return _merge_sort(xs[:])
