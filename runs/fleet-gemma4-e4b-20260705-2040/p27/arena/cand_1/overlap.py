def count_overlapping(haystack, needle):
    """
    Counts the number of overlapping occurrences of 'needle' in 'haystack'.

    Args:
        haystack (str): The string to search within.
        needle (str): The substring to search for.

    Returns:
        int: The count of overlapping occurrences. Returns 0 if needle is empty.
    """
    if not needle:
        return 0

    count = 0
    len_h = len(haystack)
    len_n = len(needle)

    # We iterate through all possible starting positions i such that the substring
    # of length len_n fits within haystack.
    # The last possible start index is len_h - len_n.
    for i in range(len_h - len_n + 1):
        if haystack[i:i + len_n] == needle:
            count += 1
            
    return count

if __name__ == '__main__':
    # Test cases based on requirements
    print(f"Test 'aa' in 'aaaa': {count_overlapping('aaaa', 'aa')}")  # Expected: 3
    print(f"Test 'a' in 'aaa': {count_overlapping('aaa', 'a')}")      # Expected: 3
    print(f"Test 'abc' in 'def': {count_overlapping('def', 'abc')}")  # Expected: 0
    print(f"Test empty needle: {count_overlapping('test', '')}")     # Expected: 0
    print(f"Test identical strings: {count_overlapping('aba', 'aba')}") # Expected: 1
    print(f"Test no match: {count_overlapping('abcde', 'xyz')}")      # Expected: 0

    # Test performance on long strings (optional check)
    long_haystack = 'a' * 1000
    print(f"Test 'aa' in 1000 'a's: {count_overlapping(long_haystack, 'aa')}") # Expected: 999

