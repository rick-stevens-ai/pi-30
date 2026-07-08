import re

def count_overlapping(haystack, needle):
    """
    Counts the number of overlapping occurrences of 'needle' in 'haystack'.
    Returns 0 if 'needle' is an empty string.
    """
    if not needle:
        return 0
    
    # Use a regex lookahead assertion (?=...) to find overlapping matches.
    # re.escape ensures that special characters in the needle are treated literally.
    # findall returns a list of matches; since we use a lookahead, each match is an empty string.
    return len(re.findall(f'(?={re.escape(needle)})', haystack))

if __name__ == "__main__":
    # Test cases
    assert count_overlapping('aaaa', 'aa') == 3
    assert count_overlapping('ababa', 'aba') == 2
    assert count_overlapping('banana', 'ana') == 2
    assert count_overlapping('mississippi', 'issi') == 2
    assert count_overlapping('aaaaa', 'aaa') == 3
    assert count_overlapping('abcde', 'f') == 0
    assert count_overlapping('', 'a') == 0
    assert count_overlapping('a', '') == 0
    assert count_overlapping('', '') == 0
    print("All tests passed!")
