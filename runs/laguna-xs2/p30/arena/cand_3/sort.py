"""Iterative bottom-up merge sort - O(n log n) time, O(n) space."""

def my_sort(xs):
    """Return a new sorted list (ascending).
    
    Handles: empty, singletons, duplicates, negatives, big ints.
    Preserves multiset. Fast on large arrays. Stdlib only.
    """
    if len(xs) <= 1:
        return list(xs)
    
    # Work on a copy
    result = list(xs)
    n = len(result)
    
    # Iterative bottom-up merge sort
    # Start with runs of size 1, double each pass
    run_size = 1
    while run_size < n:
        for start in range(0, n, 2 * run_size):
            mid = min(start + run_size, n)
            end = min(start + 2 * run_size, n)
            
            # Merge result[start:mid] and result[mid:end]
            left = result[start:mid]
            right = result[mid:end]
            
            i = j = 0
            k = start
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result[k] = left[i]
                    i += 1
                else:
                    result[k] = right[j]
                    j += 1
                k += 1
            
            # Copy remaining
            while i < len(left):
                result[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                result[k] = right[j]
                j += 1
                k += 1
        
        run_size *= 2
    
    return result