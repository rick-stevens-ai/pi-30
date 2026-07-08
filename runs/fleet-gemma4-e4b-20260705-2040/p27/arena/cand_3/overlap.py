def count_overlapping(haystack, needle):
    """
    Counts the number of OVERLAPPING occurrences of needle in haystack.
    Example: count_overlapping('aaaa', 'aa') == 3
    
    Args:
        haystack (str): The string to search within.
        needle (str): The substring to count.

    Returns:
        int: The number of overlapping occurrences.
    """
    n = len(needle)
    h_len = len(haystack)

    # Handle edge cases as required
    if n == 0 or n > h_len:
        return 0

    count = 0
    # We iterate up to the point where a full needle can still fit.
    # The loop goes from i=0 up to h_len - n inclusive.
    for i in range(h_len - n + 1):
        # Check if the substring starting at i matches the needle
        if haystack[i:i+n] == needle:
            count += 1
    
    return count

if __name__ == '__main__':
    # Test cases based on requirements
    print(f"Test 'aaaa', 'aa': {count_overlapping('aaaa', 'aa')} (Expected: 3)")
    print(f"Test 'abababa', 'aba': {count_overlapping('abababa', 'aba')} (Expected: 3)") # aba at 0, 2, 4
    print(f"Test 'abcde', 'fg': {count_overlapping('abcde', 'fg')} (Expected: 0)")
    print(f"Test 'hello', '': {count_overlapping('hello', '')} (Expected: 0) - Empty needle")
    print(f"Test '', 'a': {count_overlapping('', 'a')} (Expected: 0) - Empty haystack")
    print(f"Test 'a', 'aa': {count_overlapping('a', 'aa')} (Expected: 0) - Needle longer than haystack")

    # Stress test check (optional, just to confirm logic holds for long strings)
    long_haystack = "a" * 100
    print(f"Test '{'a'*100}', 'a': {count_overlapping(long_haystack, 'a')} (Expected: 100)")

