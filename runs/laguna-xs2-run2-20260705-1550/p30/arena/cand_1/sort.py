"""Iterative bottom-up merge sort - distinct non-recursive approach."""

def my_sort(xs):
    """Return a new sorted list (ascending).
    
    Correct on all edge cases: empty, singletons, dupes, negatives, big ints.
    Preserves multiset (stable). Fast O(n log n) on large arrays.
    Stdlib only.
    """
    if not xs or len(xs) < 2:
        return list(xs)
    
    # Start with each element as a sorted "run" of size 1
    # Use a list of runs to avoid recursion
    runs = [[x] for x in xs]
    
    # Iteratively merge adjacent runs until one remains
    while len(runs) > 1:
        merged = []
        i = 0
        while i < len(runs):
            if i + 1 < len(runs):
                merged.append(_merge_two(runs[i], runs[i + 1]))
                i += 2
            else:
                merged.append(runs[i])
                i += 1
        runs = merged
    
    return runs[0]


def _merge_two(a, b):
    """Merge two sorted lists into one sorted list (stable)."""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result