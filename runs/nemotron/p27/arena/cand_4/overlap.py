"""Overlapping substring count — Candidate #4: regex lookahead (C-speed, concise)."""

import re


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return number of OVERLAPPING occurrences of needle in haystack.

    Examples:
        count_overlapping("aaaa", "aa") == 3
        count_overlapping("abc", "") == 0
        count_overlapping("", "a") == 0
    """
    if not needle:
        return 0

    # Positive lookahead (?=...) finds overlapping matches.
    # re.escape handles regex metacharacters in needle.
    pattern = f"(?={re.escape(needle)})"
    return len(re.findall(pattern, haystack))


if __name__ == "__main__":
    # Quick sanity checks
    assert count_overlapping("aaaa", "aa") == 3
    assert count_overlapping("abababa", "aba") == 3
    assert count_overlapping("abc", "") == 0
    assert count_overlapping("", "a") == 0
    assert count_overlapping("hello", "world") == 0
    assert count_overlapping("aaa", "a") == 3
    assert count_overlapping("mississippi", "iss") == 2
    print("All tests passed.")