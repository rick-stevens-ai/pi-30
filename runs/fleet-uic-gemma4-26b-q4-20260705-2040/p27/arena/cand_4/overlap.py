import re

def count_overlapping(haystack: str, needle: str) -> int:
    """
    Returns the number of overlapping occurrences of needle in haystack.
    If needle is empty, returns 0.

    This implementation uses a regex positive lookahead assertion to find
    all starting positions of the needle without consuming characters, 
    enabling detection of overlapping matches efficiently using stdlib's re module.
    """
    if not needle:
        return 0
    
    # (?=...) is a zero-width positive lookahead assertion.
    # It matches a position where the pattern follows, but does not consume characters.
    # re.escape handles special regex characters in the needle to treat it as a literal.
    pattern = f'(?={re.escape(needle)})'
    return len(re.findall(pattern, haystack))

if __name__ == "__main__":
    # Basic verification per requirements
    assert count_overlapping('aaaa', 'aa') == 3  # (0:aa.., 1:.aa., 2:..aa)
    assert count_overlapping('banana', 'ana') == 2 # (1:ana, 3:ana)
    assert count_overlapping('abcde', 'f') == 0
    assert count_overlapping('aaaaa', '') == 0     # Empty needle requirement
    assert count_overlapping('', 'a') == 0
    assert count_overlapping('', '') == 0
    
    print("All basic tests passed.")
