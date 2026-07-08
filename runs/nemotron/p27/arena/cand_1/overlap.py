"""Count overlapping occurrences of needle in haystack."""

import re


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of overlapping occurrences of needle in haystack.

    Args:
        haystack: String to search in.
        needle: Substring to count. Empty needle returns 0.

    Returns:
        Count of overlapping occurrences.

    Examples:
        >>> count_overlapping("aaaa", "aa")
        3
        >>> count_overlapping("ababa", "aba")
        2
        >>> count_overlapping("hello", "")
        0
    """
    if not needle:
        return 0
    # Use regex lookahead to find overlapping matches
    # re.escape handles special regex chars in needle
    pattern = f"(?={re.escape(needle)})"
    return len(re.findall(pattern, haystack))


if __name__ == "__main__":
    # Quick sanity checks
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("ababa", "aba") == 2
    assert count_overlapping("hello", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("abc", "abc") == 1
    assert count_overlapping("aaaaa", "aaa") == 3
    print("All tests passed.")