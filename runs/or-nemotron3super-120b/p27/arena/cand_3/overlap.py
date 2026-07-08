import re

def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of overlapping occurrences of needle in haystack.
    Returns 0 for an empty needle.
    Uses a regex look‑ahead to find all start positions, which runs in
    O(n + m) time (where n = len(haystack), m = len(needle)) and uses
    only the standard library.

    Example:
        >>> count_overlapping("aaaa", "aa")
        3
        >>> count_overlapping("ababa", "aba")
        2
        >>> count_overlapping("hello", "ll")
        1
        >>> count_overlapping("hello", "")
        0
    """
    if not needle:
        return 0
    # Escape needle so that any regex metacharacters are treated literally.
    pattern = f'(?={re.escape(needle)})'
    # re.findall returns a list of the captured groups; for a look‑ahead
    # with no capturing group each element is an empty string, one per match.
    return len(re.findall(pattern, haystack))


if __name__ == "__main__":
    # Simple sanity checks
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("ababa", "aba") == 2
    assert count_overlapping("hello", "ll") == 1
    assert count_overlapping("hello", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("", "") == 0
    print("All internal tests passed.")