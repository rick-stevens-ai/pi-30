"""Radix sort implementation - distinct from typical comparison-based sorts."""
from typing import List, Any


def _counting_sort_by_digit(arr: List[int], exp: int) -> List[int]:
    """Stable counting sort for a specific digit position."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    # Store count of occurrences
    for num in arr:
        digit = (abs(num) // exp) % 10
        count[digit] += 1
    
    # Change count to cumulative
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array (reverse for stability)
    for i in range(n - 1, -1, -1):
        num = arr[i]
        digit = (abs(num) // exp) % 10
        output[count[digit] - 1] = num
        count[digit] -= 1
    
    return output


def _radix_sort_positive(arr: List[int]) -> List[int]:
    """Radix sort for non-negative integers."""
    if not arr:
        return []
    
    # Find maximum number to determine number of digits
    max_num = max(arr)
    
    # Do counting sort for every digit
    exp = 1
    result = arr[:]
    while max_num // exp > 0:
        result = _counting_sort_by_digit(result, exp)
        exp *= 10
    
    return result


def my_sort(xs: List[Any]) -> List[Any]:
    """
    Sort a list of integers in ascending order using radix sort.
    
    Time complexity: O(n * k) where k is number of digits in max value.
    Space complexity: O(n).
    
    Handles: empty lists, singletons, duplicates, negatives, big integers.
    Preserves multiset exactly.
    """
    if not xs:
        return []
    
    # Validate all elements are integers
    for x in xs:
        if not isinstance(x, int):
            raise TypeError(f"Expected int, got {type(x).__name__}")
    
    # Separate negative and non-negative numbers
    negatives = [x for x in xs if x < 0]
    non_negatives = [x for x in xs if x >= 0]
    
    # Sort negatives: sort absolute values, then negate and reverse
    # (so -5, -2, -1 instead of -1, -2, -5)
    neg_abs = [abs(x) for x in negatives]
    sorted_negs = _radix_sort_positive(neg_abs)
    sorted_negs = [-x for x in reversed(sorted_negs)]
    
    # Sort non-negatives directly
    sorted_non_negs = _radix_sort_positive(non_negatives)
    
    return sorted_negs + sorted_non_negs