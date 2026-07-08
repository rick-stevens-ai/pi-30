"""Base-256 radix sort implementation - distinct from comparison-based sorts."""


def my_sort(xs):
    """Return a new sorted list (ascending) using base-256 radix sort.
    
    Correct on all edge cases: empty, singletons, dupes, negatives, big ints.
    Preserves multiset. O(n*k) where k = bytes needed for max value.
    Stdlib only. Uses LSD radix sort - distinct from quicksort/mergesort.
    """
    if len(xs) <= 1:
        return list(xs)
    
    # Separate negatives from non-negatives
    negatives = [x for x in xs if x < 0]
    non_negatives = [x for x in xs if x >= 0]
    
    # Negatives: sort by absolute value ascending, then reverse and negate
    negatives = [-x for x in negatives]
    negatives = _radix_sort_base256(negatives)
    negatives = [-x for x in reversed(negatives)]
    
    # Non-negatives: sort directly
    non_negatives = _radix_sort_base256(non_negatives)
    
    return negatives + non_negatives


def _radix_sort_base256(nums):
    """LSD radix sort using base 256 (byte-wise)."""
    if not nums:
        return []
    
    result = list(nums)
    max_val = max(result)
    
    if max_val == 0:
        return result
    
    # Process each byte position (256 possible values = efficient counting sort)
    byte_pos = 0
    while (max_val >> (byte_pos * 8)) > 0:
        result = _counting_sort_by_byte(result, byte_pos)
        byte_pos += 1
    
    return result


def _counting_sort_by_byte(nums, byte_pos):
    """Stable counting sort by byte position."""
    n = len(nums)
    output = [0] * n
    count = [0] * 256
    
    mask = 0xFF
    shift = byte_pos * 8
    
    # Count occurrences
    for num in nums:
        byte_val = (num >> shift) & mask
        count[byte_val] += 1
    
    # Cumulative count
    total = 0
    for i in range(256):
        old_count = count[i]
        count[i] = total
        total += old_count
    
    # Build output
    for num in nums:
        byte_val = (num >> shift) & mask
        output[count[byte_val]] = num
        count[byte_val] += 1
    
    return output