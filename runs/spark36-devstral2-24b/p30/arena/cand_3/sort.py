"""
Sorting implementation using a non-comparison-based approach.
Implements the radix sort algorithm for integral types.
This achieves O(n) time complexity in most practical cases.

Edge Cases Handled:
- Empty lists return empty list
- Single element lists are returned unchanged
- Duplicate values are preserved correctly (stable sort)
- Negative numbers handled properly through sign analysis
"""

def my_sort(xs):
    """Return a new sorted list in ascending order using radix sort."""
    if not xs:
        return []
    
    # Check if all values are the same
    first_val = xs[0]
    all_same = True
    for x in xs[1:]:
        if x != first_val:
            all_same = False
            break
    
    if all_same:
        return list(xs)  # Defensive copy
    
    # Handle empty and singleton cases
    if len(xs) == 1:
        return list(xs)
    
    # Find the minimum value to handle negative numbers
    min_val = min(xs)
    
    if min_val >= 0:
        return radix_sort_positive(xs)
    else:
        return radix_sort_with_negatives(xs, min_val)


def radix_sort_positive(arr):
    """Perform radix sort on non-negative integers."""
    # Find the maximum number to know number of digits
    max_num = max(arr)
    
    # Do counting sort for every digit
    exp = 1  # Current place value
    while max_num // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr if len(arr) == 1 else arr.copy()


def radix_sort_with_negatives(arr, min_val):
    """Handle negative numbers by transforming them to positive."""
    transformed = [x - min_val for x in arr]
    sorted_trans = radix_sort_positive(transformed)
    return [x + (-min_val) for x in sorted_trans]


def counting_sort_by_digit(arr, exp):
    """Counting sort of arr based on the digit represented by exp."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    # Store count of occurrences in count[]
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    
    # Change count[i] so that count[i] now contains actual position of this digit in output[]
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build the output array (stable sort)
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1
    
    # Copy the output array to arr, so that arr now contains sorted numbers according to current digit
    for i in range(n):
        arr[i] = output[i]
