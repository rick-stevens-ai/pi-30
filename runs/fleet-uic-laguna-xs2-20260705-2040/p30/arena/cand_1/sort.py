"""Hybrid sort - counting sort for small ranges, radix sort for large, distinct approach."""


def my_sort(xs):
    """
    Sort a list of integers in ascending order using an adaptive hybrid approach.
    
    Strategy:
    1. Counting sort for small integer ranges (O(n + range), very fast when range is small)
    2. Radix sort for larger integers (O(n * k) where k is digit count)
    3. Distinct from comparison sorts: non-comparison-based for most cases
    
    Args:
        xs: List of integers (can be empty, contain duplicates, negatives, or big ints)
        
    Returns:
        A new sorted list in ascending order, preserving the multiset.
    """
    if len(xs) <= 1:
        return list(xs)
    
    # Separate negatives and non-negatives
    negatives = [x for x in xs if x < 0]
    non_negatives = [x for x in xs if x >= 0]
    
    # Sort negatives: make positive, sort, then negate and reverse
    if negatives:
        negatives = [-x for x in negatives]
        negatives = _sort_nonneg(negatives)
        negatives = [-x for x in reversed(negatives)]
    
    # Sort non-negatives directly
    if non_negatives:
        non_negatives = _sort_nonneg(non_negatives)
    
    return negatives + non_negatives


def _sort_nonneg(arr):
    """Sort non-negative integers using the best algorithm for the data."""
    n = len(arr)
    if n <= 1:
        return list(arr)
    
    min_val, max_val = min(arr), max(arr)
    range_size = max_val - min_val + 1
    
    # Counting sort is fastest when range is O(n) - very cache-friendly
    # Use threshold based on available memory (2^20 = 1M entries ~ 8MB)
    if range_size <= 2**20 and range_size <= n * 10:
        return _counting_sort(arr, min_val, max_val)
    
    # Otherwise use radix sort
    return _radix_sort_lsd(arr)


def _counting_sort(arr, min_val, max_val):
    """Counting sort for small ranges - extremely fast O(n + range)."""
    n = len(arr)
    offset = min_val
    range_size = max_val - min_val + 1
    
    count = [0] * range_size
    for num in arr:
        count[num - offset] += 1
    
    output = [0] * n
    pos = 0
    for i, c in enumerate(count):
        output[pos:pos + c] = [i + offset] * c
        pos += c
    
    return output


def _radix_sort_lsd(arr):
    """
    LSD (Least Significant Digit) radix sort for non-negative integers.
    
    Uses base 2^16 (word-wise) for efficiency with Python's arbitrary precision ints.
    """
    n = len(arr)
    if n <= 1:
        return list(arr)
    
    max_val = max(arr)
    
    exp = 1
    result = list(arr)
    base = 2**16
    
    while max_val // exp > 0:
        result = _counting_sort_by_digit(result, exp, base)
        exp *= base
    
    return result


def _counting_sort_by_digit(arr, exp, base):
    """Counting sort for a specific digit position - stable."""
    n = len(arr)
    output = [0] * n
    count = [0] * base
    
    for num in arr:
        digit = (num // exp) % base
        count[digit] += 1
    
    for i in range(1, base):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % base
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    return output