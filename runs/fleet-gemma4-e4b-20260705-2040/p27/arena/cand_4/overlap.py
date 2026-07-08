def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of needle in haystack.

    Args:
        haystack: The string to search within.
        needle: The substring to search for.

    Returns:
        The number of overlapping occurrences. Returns 0 if needle is empty.
    """
    if not needle:
        return 0

    count = 0
    len_h = len(haystack)
    len_n = len(needle)

    # Iterate through all possible starting positions where needle could fit.
    # The loop runs from index 0 up to len_h - len_n, inclusive.
    for i in range(len_h - len_n + 1):
        # Check if the substring of haystack matches the needle
        if haystack[i:i + len_n] == needle:
            count += 1

    return count

if __name__ == '__main__':
    # Test cases provided in prompt
    print(f"Test 'aaaa', 'aa': {count_overlapping('aaaa', 'aa')}") # Expected: 3
    
    # Additional test cases
    print(f"Test 'banana', 'ana': {count_overlapping('banana', 'ana')}") # Expected: 2 (b[ana]na, ban[ana]) -> wait, banana has two overlapping instances? No. b-a-n-a-n-a. Index 1: ana. Index 3: ana. Total 2.
    print(f"Test 'ababab', 'aba': {count_overlapping('ababab', 'aba')}") # Expected: 2 (Index 0, Index 2)
    print(f"Test 'aaaaa', 'aa': {count_overlapping('aaaaa', 'aa')}") # Expected: 4 (Indices 0, 1, 2, 3)
    print(f"Test 'abcde', 'xyz': {count_overlapping('abcde', 'xyz')}") # Expected: 0
    print(f"Test 'test', '': {count_overlapping('test', '')}") # Expected: 0 (Empty needle case)
    print(f"Test '', 'a': {count_overlapping('', 'a')}") # Expected: 0
