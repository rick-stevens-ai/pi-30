"""overlap.py - expose count_overlapping(haystack, needle) -> int

Count overlapping occurrences of `needle` in `haystack`.
- If `needle` is empty → 0
- Overlapping matches are counted (e.g. 'aa' in 'aaaa' yields 3)
- Uses only the Python standard library and is efficient for long strings.
"""

import re


def count_overlapping(haystack: str, needle: str) -> int:
    """
    Return the number of overlapping occurrences of `needle` in `haystack`.

    Parameters
    ----------
    haystack : str
        The string to search within.
    needle : str
        The substring to search for.

    Returns
    -------
    int
        Number of (possibly overlapping) matches.  Zero if `needle`
        is empty or does not occur.

    Examples
    --------
    >>> count_overlapping('aaaa', 'aa')
    3
    >>> count_overlapping('hello', 'll')
    1
    >>> count_overlapping('abababa', 'aba')
    2
    """
    # Empty needle per specification yields 0 matches.
    if not needle:
        return 0

    # Escape the needle so that any regex meta‑characters are treated literally.
    escaped = re.escape(needle)

    # Use a positive look‑ahead pattern to find overlapping matches.
    # `(?=pattern)` is zero‑width, so each match consumes no characters,
    # allowing the next search to start at the next character position.
    pattern = f'(?={escaped})'

    # `re.finditer` yields an iterator over all non‑overlapping *positions*
    # where the look‑ahead succeeds. Counting them gives the overlapping
    # occurrence count efficiently (implemented in C).
    return sum(1 for _ in re.finditer(pattern, haystack))


# ---------------------------------------------------------------------------
# Simple demo / self‑test when the module is executed directly.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        ("aaaa", "aa", 3),
        ("hello", "ll", 1),
        ("abababa", "aba", 2),
        ("", "a", 0),
        ("abc", "", 0),
        ("aaaaa", "aaaa", 2),
    ]

    for hay, needle, expected in test_cases:
        result = count_overlapping(hay, needle)
        assert result == expected, f"Failed: {hay!r}, {needle!r} → {result}, expected {expected}"
    print("All tests passed.")