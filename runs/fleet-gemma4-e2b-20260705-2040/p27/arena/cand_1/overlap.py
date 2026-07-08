def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of needle in haystack.

    Args:
        haystack: The string to search within.
        needle: The pattern to search for.

    Returns:
        The total number of overlapping occurrences. Returns 0 if needle is empty.
    """
    if not needle:
        return 0

    n = len(haystack)
    m = len(needle)

    if m == 0 or n < m:
        return 0

    count = 0
    current_search_start = 0

    while True:
        # Find the next occurrence of needle starting from current_search_start
        found_index = haystack.find(needle, current_search_start)

        if found_index == -1:
            # No more occurrences found
            break

        count += 1

        # To allow overlapping matches, start the next search one position after the start of the found match
        current_search_start = found_index + 1

    return count

if __name__ == '__main__':
    # Test case: 'aa' in 'aaaa' should be 3 (at indices 0, 1, 2)
    print(f"'aaaa', 'aa': {count_overlapping('aaaa', 'aa')}")  # Expected: 3

    # Test case: Overlapping at the start and end
    print(f"'abababa', 'aba': {count_overlapping('abababa', 'aba')}") # aba at 0, 2, 4. Expected: 3

    # Test case: No overlap
    print(f"'abcde', 'xyz': {count_overlapping('abcde', 'xyz')}")  # Expected: 0

    # Test case: Empty needle (must be 0)
    print(f"'abc', '': {count_overlapping('abc', '')}")          # Expected: 0

    # Test case: Needle longer than haystack
    print(f"'a', 'aa': {count_overlapping('a', 'aa')}")          # Expected: 0

    # Test case: Full overlap
    print(f"'abc', 'abc': {count_overlapping('abc', 'abc')}")      # Expected: 1