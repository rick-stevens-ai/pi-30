import re

def count_overlapping(haystack, needle):
    """
    Counts overlapping occurrences of needle in haystack.
    Returns 0 if needle is empty.
    """
    if not needle:
        return 0
    # Use a lookahead assertion to find all overlapping matches.
    # re.escape ensures that special regex characters in the needle are treated literally.
    # The lookahead (?=...) matches at a position without consuming any characters,
    # allowing us to find every starting position where the needle occurs.
    return len(re.findall(f'(?={re.escape(needle)})', haystack))

if __name__ == "__main__":
    # Test cases
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("banana", "ana") == 2
    assert count_overlapping("mississippi", "issi") == 2
    assert count_overlapping("abcde", "f") == 0
    assert count_overlapping("aaaaa", "aaa") == 3
    assert count_overlapping("hello", "") == 0
    assert count_overlapping("", "hello") == 0
    assert count_overlapping("", "") == 0
    print("All tests passed!")
