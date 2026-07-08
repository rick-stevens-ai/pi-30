def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of needle in haystack.

    Args:
        haystack: The string to search within.
        needle: The pattern to search for.

    Returns:
        The number of overlapping occurrences. Returns 0 if needle is empty.
    """
    if not needle:
        return 0

    count = 0
    n_len = len(needle)
    h_len = len(haystack)

    if n_len == 0 or h_len < n_len:
        return 0

    # Iterate through all possible starting positions for the needle.
    # We stop at h_len - n_len because any further start position won't fit the needle.
    for i in range(h_len - n_len + 1):
        if haystack[i:i + n_len] == needle:
            count += 1

    return count

if __name__ == '__main__':
    # Test case 1: Overlapping example (as per prompt)
    print(f"'aa' in 'aaaa': {count_overlapping('aaaa', 'aa')}")  # Expected: 3

    # Test case 2: Standard non-overlapping check (for comparison)
    print(f"'ab' in 'ababab': {count_overlapping('ababab', 'ab')}") # Expected: 3 (at 0, 2, 4) - Wait, let's re-check logic.
    # 'ababab', needle='ab' (len=2). h_len=6. range(5) -> i=0..4
    # i=0: 'ab' -> count=1
    # i=1: 'ba'
    # i=2: 'ab' -> count=2
    # i=3: 'ba'
    # i=4: 'ab' -> count=3. Expected: 3. Correct.

    # Test case 3: Empty needle (must be 0)
    print(f"'a' in '': {count_overlapping('', 'a')}") # Expected: 0
    print(f"'a' in '': {count_overlapping('', '')}") # Expected: 0

    # Test case 4: Needle longer than haystack
    print(f"'abc' in 'ab': {count_overlapping('ab', 'abc')}") # Expected: 0

    # Test case 5: No match
    print(f"'x' in 'abcde': {count_overlapping('abcde', 'x')}") # Expected: 0

    # Test case 6: Full match
    print(f"'abc' in 'abc': {count_overlapping('abc', 'abc')}") # Expected: 1