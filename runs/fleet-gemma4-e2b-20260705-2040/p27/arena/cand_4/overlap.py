def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of needle in haystack.
    Returns 0 if needle is empty.

    Args:
        haystack: The string to search within.
        needle: The substring to search for.

    Returns:
        The total number of overlapping occurrences.
    """
    if not needle:
        return 0

    count = 0
    n = len(haystack)
    m = len(needle)

    if m == 0 or n < m:
        return 0

    # Iterate through all possible starting positions for the needle
    for i in range(n - m + 1):
        if haystack[i:i + m] == needle:
            count += 1
    
    return count

if __name__ == '__main__':
    # Example 1: Overlapping case (aa in aaaa -> 3)
    print(f"'aaaa', 'aa': {count_overlapping('aaaa', 'aa')}") # Expected: 3
    
    # Example 2: Standard non-overlapping (banana, ana -> 2)
    print(f"'banana', 'ana': {count_overlapping('banana', 'ana')}") # Expected: 2
    
    # Example 3: Empty needle case
    print(f"'test', '': {count_overlapping('test', '')}") # Expected: 0

    # Example 4: Needle longer than haystack
    print(f"'a', 'aa': {count_overlapping('a', 'aa')}") # Expected: 0
