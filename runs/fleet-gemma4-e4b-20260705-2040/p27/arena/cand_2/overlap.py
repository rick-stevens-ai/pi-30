def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of 'needle' in 'haystack'.

    Args:
        haystack: The string to search within.
        needle: The substring to search for.

    Returns:
        The total count of overlapping occurrences. Returns 0 if needle is empty.
    """
    if not needle:
        return 0

    M = len(needle)
    N = len(haystack)
    count = 0

    # Iterate through all possible starting positions i in the haystack
    # We stop at N - M, as any position after this would result in a slice shorter than M.
    for i in range(N - M + 1):
        if haystack[i:i+M] == needle:
            count += 1

    return count

if __name__ == '__main__':
    # Test cases provided by user/problem description
    print(f"Test 1 (aa in aaaa): {count_overlapping('aaaa', 'aa')}") # Expected: 3
    print(f"Test 2 (a in aaa): {count_overlapping('aaa', 'a')}")   # Expected: 3
    print(f"Test 3 (abc in abcd): {count_overlapping('abcd', 'abc')}") # Expected: 1
    print(f"Test 4 (no match): {count_overlapping('abc', 'xyz')}")  # Expected: 0
    print(f"Test 5 (empty needle): {count_overlapping('abc', '')}")   # Expected: 0
    print(f"Test 6 (needle longer than haystack): {count_overlapping('a', 'aa')}") # Expected: 0
    print(f"Test 7 (single char match): {count_overlapping('x', 'x')}") # Expected: 1