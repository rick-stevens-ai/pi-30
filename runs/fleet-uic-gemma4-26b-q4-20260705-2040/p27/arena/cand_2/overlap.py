import re

def count_overlapping(haystack: str, needle: str) -> int:
    """
    Counts the number of overlapping occurrences of needle in haystack.
    Returns 0 if needle is empty.
    Uses a lookahead regex for performance on long strings.
    """
    if not needle:
        return 0
    # re.escape ensures that special characters in needle are treated as literals.
    # Using a positive lookahead (?=...) allows the engine to find overlapping matches.
    return len(re.findall(f'(?={re.escape(needle)})', haystack))

if __name__ == "__main__":
    # Test cases
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("banana", "ana") == 2
    assert count_overlapping("aaaaa", "aaa") == 3
    assert count_overlapping("abcde", "f") == 0
    assert count_overlapping("aaaaa", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("", "") == 0
    # Test special characters
    assert count_overlapping("a.b.c", ".") == 2
    assert count_overlapping("a*b*", "*") == 2
    print("All tests passed!")
